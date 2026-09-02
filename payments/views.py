from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from users.decorators import role_required
from students.models import Student
from academics.models import CourseEnrollment
from .models import Invoice, Payment, AdminBankAccount, AdminQrisSetting
from django import forms
from .forms import InvoiceForm, CashPaymentForm, AdminBankAccountForm, AdminQrisForm
from .utils import generate_invoice_pdf, generate_receipt_pdf
from django.http import HttpResponse
from notifications.utils import create_notification

class PaymentSubmitForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'payment_reference', 'proof']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Jumlah Transfer', 'step': '0.01'}),
            'payment_method': forms.Select(
                choices=[('BANK_TRANSFER', 'Transfer Bank'), ('QRIS', 'Scan QRIS')],
                attrs={'class': 'form-control default-select wide', 'id': 'id_payment_method'}
            ),
            'payment_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Pengirim / No. Referensi'}),
            'proof': forms.FileInput(attrs={'class': 'form-control'}),
        }

@login_required(login_url='getskills:login')
@role_required(['STUDENT'])
def student_invoice_list(request):
    try:
        student_profile = request.user.student_profile
        invoices = Invoice.objects.filter(student=student_profile).order_by('-due_date')
        today = timezone.now().date()
        for invoice in invoices:
            start_payment_date = invoice.due_date.replace(day=1)
            invoice.can_pay = today >= start_payment_date or today >= invoice.created_at.date()
            invoice.has_pending_payment = invoice.payments.filter(status='PENDING').exists()
    except Student.DoesNotExist:
        invoices = []
        messages.error(request, "Profil siswa tidak ditemukan.")
    
    context = {
        "invoices": invoices,
        "page_title": "Daftar Tagihan"
    }
    return render(request, 'payments/student_invoice_list.html', context)

@login_required(login_url='getskills:login')
@role_required(['STUDENT'])
def student_pay_invoice(request, invoice_id):
    student_profile = request.user.student_profile
    invoice = get_object_or_404(Invoice, id=invoice_id, student=student_profile)
    
    # Check if payment is allowed (only starting from the 1st of the due date month)
    today = timezone.now().date()
    start_payment_date = invoice.due_date.replace(day=1)
    if today < start_payment_date and today < invoice.created_at.date():
        messages.warning(request, f"Pembayaran untuk tagihan ini baru dapat dilakukan mulai tanggal {start_payment_date.strftime('%d-%m-%Y')}.")
        return redirect('payments:student_invoice_list')
        
    if invoice.status == 'PAID':
        messages.info(request, "Tagihan ini sudah lunas.")
        return redirect('payments:student_invoice_list')
        
    bank_accounts = AdminBankAccount.objects.filter(status=True)
    qris_settings = AdminQrisSetting.objects.filter(status=True)
    pending_payment = Payment.objects.filter(invoice=invoice, status='PENDING').first()
    
    if request.method == 'POST':
        form = PaymentSubmitForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.student = student_profile
            if not payment.payment_method:
                payment.payment_method = 'BANK_TRANSFER'
            payment.status = 'PENDING'
            payment.save()
            
            messages.success(request, f"Bukti pembayaran ({payment.get_payment_method_display()}) berhasil diunggah. Menunggu verifikasi dari admin.")
            return redirect('payments:student_invoice_list')
    else:
        form = PaymentSubmitForm(initial={'amount': invoice.amount, 'payment_method': 'BANK_TRANSFER'})
        
    context = {
        "invoice": invoice,
        "bank_accounts": bank_accounts,
        "qris_settings": qris_settings,
        "form": form,
        "pending_payment": pending_payment,
        "page_title": "Bayar Tagihan"
    }
    return render(request, 'payments/student_pay_invoice.html', context)

@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_payment_verification(request):
    pending_payments = Payment.objects.filter(status='PENDING').order_by('-created_at')
    context = {
        "pending_payments": pending_payments,
        "page_title": "Verifikasi Pembayaran"
    }
    return render(request, 'payments/admin_payment_verification.html', context)

@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_verify_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    action = request.POST.get('action')
    
    if payment.status != 'PENDING':
        messages.warning(request, "Pembayaran ini sudah diproses sebelumnya.")
        return redirect('payments:admin_payment_verification')
        
    if action == 'approve':
        payment.status = 'VERIFIED'
        payment.paid_at = timezone.now()
        payment.verified_by = request.user
        payment.verified_at = timezone.now()
        payment.save()
        
        # Lunas
        invoice = payment.invoice
        invoice.status = 'PAID'
        invoice.save()
        
        # Notify Student
        create_notification(
            user=payment.student.user,
            title="Pembayaran Berhasil Terverifikasi",
            message=f"Pembayaran untuk Invoice {invoice.invoice_number} sebesar Rp {payment.amount} telah berhasil diverifikasi.",
            notification_type='PAYMENT'
        )
        
        messages.success(request, f"Pembayaran untuk Invoice {invoice.invoice_number} disetujui. Tagihan lunas.")
    elif action == 'reject':
        payment.status = 'FAILED'
        payment.verified_by = request.user
        payment.verified_at = timezone.now()
        payment.save()
        messages.warning(request, f"Pembayaran untuk Invoice {payment.invoice.invoice_number} ditolak.")
        
    return redirect('payments:admin_payment_verification')


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_trigger_billing(request):
    if request.method == 'POST':
        today = timezone.now().date()
        year = today.year
        month = today.month
        month_str = today.strftime('%m')
        
        # Get all active enrollments
        active_enrollments = CourseEnrollment.objects.filter(status='ACTIVE')
        created_count = 0
        skipped_count = 0
        
        import datetime
        for enrollment in active_enrollments:
            student = enrollment.student
            course = enrollment.course
            
            # Formulate unique invoice number
            invoice_num = f"INV-{student.student_code}-{course.code}-{year}{month_str}"
            
            # Check if this invoice already exists to prevent duplicate billing
            if Invoice.objects.filter(invoice_number=invoice_num).exists():
                skipped_count += 1
                continue
                
            # Due date is set to the 10th of the current month
            due_date = datetime.date(year, month, 10)
            
            # Create Invoice
            invoice = Invoice.objects.create(
                invoice_number=invoice_num,
                student=student,
                course=course,
                amount=course.price,
                due_date=due_date,
                status='UNPAID'
            )
            
            # Notify Student
            create_notification(
                user=student.user,
                title="Tagihan Pembayaran Baru",
                message=f"Tagihan baru {invoice.invoice_number} sebesar Rp {invoice.amount} telah diterbitkan untuk program {course.name}. Jatuh tempo: {due_date.strftime('%d-%m-%Y')}.",
                notification_type='PAYMENT'
            )
            
            created_count += 1
            
        messages.success(
            request, 
            f"Proses tagihan bulanan selesai. Berhasil mencetak {created_count} invoice baru. {skipped_count} invoice dilewati karena sudah ada."
        )
    return redirect('payments:admin_invoice_list')


# Invoices
@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_at')
    context = {
        'invoices': invoices,
        'page_title': 'Manajemen Invoice'
    }
    return render(request, 'payments/admin_invoice_list.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            
            # Notify Student
            create_notification(
                user=invoice.student.user,
                title="Tagihan Pembayaran Baru",
                message=f"Tagihan baru {invoice.invoice_number} sebesar Rp {invoice.amount} telah diterbitkan. Jatuh tempo: {invoice.due_date.strftime('%d-%m-%Y')}.",
                notification_type='PAYMENT'
            )
            
            messages.success(request, f"Invoice {invoice.invoice_number} berhasil dibuat.")
            return redirect('payments:admin_invoice_list')
    else:
        form = InvoiceForm()
        
    context = {
        'form': form,
        'page_title': 'Buat Tagihan Pembayaran Baru',
        'cancel_url': '/payments/admin-invoices/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, f"Invoice {invoice.invoice_number} berhasil diperbarui.")
            return redirect('payments:admin_invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
        
    context = {
        'form': form,
        'page_title': f"Edit Invoice {invoice.invoice_number}",
        'cancel_url': '/payments/admin-invoices/'
    }
    return render(request, 'projects/project_form.html', context)


# Payments
@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_payment_list(request):
    payments = Payment.objects.all().order_by('-created_at')
    context = {
        'payments': payments,
        'page_title': 'Riwayat Pembayaran'
    }
    return render(request, 'payments/admin_payment_list.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_record_cash_payment(request):
    if request.method == 'POST':
        form = CashPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.payment_method = 'CASH'
            payment.status = 'VERIFIED'
            payment.paid_at = timezone.now()
            payment.verified_by = request.user
            payment.verified_at = timezone.now()
            payment.save()
            
            # Mark invoice as paid
            invoice = payment.invoice
            invoice.status = 'PAID'
            invoice.save()
            
            messages.success(request, f"Pembayaran cash untuk invoice {invoice.invoice_number} berhasil dicatat dan diverifikasi.")
            return redirect('payments:admin_payment_list')
    else:
        form = CashPaymentForm(initial={'paid_at': timezone.now()})
        
    context = {
        'form': form,
        'page_title': 'Catat Pembayaran Cash',
        'cancel_url': '/payments/admin-payments/'
    }
    return render(request, 'projects/project_form.html', context)


# Bank Accounts
@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_bank_account_list(request):
    accounts = AdminBankAccount.objects.all().order_by('bank_name')
    context = {
        'accounts': accounts,
        'page_title': 'Rekening Penerima'
    }
    return render(request, 'payments/admin_bank_account_list.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_add_bank_account(request):
    if request.method == 'POST':
        form = AdminBankAccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            messages.success(request, f"Rekening {account.bank_name} berhasil ditambahkan.")
            return redirect('payments:admin_bank_account_list')
    else:
        form = AdminBankAccountForm()
        
    context = {
        'form': form,
        'page_title': 'Tambah Rekening Bank',
        'cancel_url': '/payments/bank-accounts/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_edit_bank_account(request, account_id):
    account = get_object_or_404(AdminBankAccount, id=account_id)
    if request.method == 'POST':
        form = AdminBankAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, f"Rekening {account.bank_name} berhasil diperbarui.")
            return redirect('payments:admin_bank_account_list')
    else:
        form = AdminBankAccountForm(instance=account)
        
    context = {
        'form': form,
        'page_title': f"Edit Rekening {account.bank_name}",
        'cancel_url': '/payments/bank-accounts/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_delete_bank_account(request, account_id):
    account = get_object_or_404(AdminBankAccount, id=account_id)
    bank_name = account.bank_name
    account.delete()
    messages.success(request, f"Rekening '{bank_name}' berhasil dihapus.")
    return redirect('payments:admin_bank_account_list')


# Custom Admin QRIS Settings
@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_qris_list(request):
    qris_list = AdminQrisSetting.objects.all().order_by('-created_at')
    context = {
        "qris_list": qris_list,
        "page_title": "Kelola QRIS Pembayaran"
    }
    return render(request, 'payments/admin_qris_list.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_add_qris(request):
    if request.method == 'POST':
        form = AdminQrisForm(request.POST, request.FILES)
        if form.is_valid():
            qris = form.save()
            messages.success(request, f"Gambar QRIS '{qris.name}' berhasil ditambahkan.")
            return redirect('payments:admin_qris_list')
    else:
        form = AdminQrisForm()
        
    context = {
        'form': form,
        'page_title': 'Tambah QRIS Pembayaran',
        'cancel_url': '/payments/qris/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_edit_qris(request, qris_id):
    qris = get_object_or_404(AdminQrisSetting, id=qris_id)
    if request.method == 'POST':
        form = AdminQrisForm(request.POST, request.FILES, instance=qris)
        if form.is_valid():
            form.save()
            messages.success(request, f"Gambar QRIS '{qris.name}' berhasil diperbarui.")
            return redirect('payments:admin_qris_list')
    else:
        form = AdminQrisForm(instance=qris)
        
    context = {
        'form': form,
        'page_title': f"Edit QRIS '{qris.name}'",
        'cancel_url': '/payments/qris/'
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='getskills:login')
@role_required(['ADMIN'])
def admin_delete_qris(request, qris_id):
    qris = get_object_or_404(AdminQrisSetting, id=qris_id)
    name = qris.name
    qris.delete()
    messages.success(request, f"QRIS '{name}' berhasil dihapus.")
    return redirect('payments:admin_qris_list')


# PDF Downloads
@login_required(login_url='getskills:login')
def download_invoice_pdf(request, invoice_id):
    if request.user.role == 'STUDENT':
        invoice = get_object_or_404(Invoice, id=invoice_id, student__user=request.user)
    else:
        invoice = get_object_or_404(Invoice, id=invoice_id)
        
    pdf_data = generate_invoice_pdf(invoice)
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice-{invoice.invoice_number}.pdf"'
    return response


@login_required(login_url='getskills:login')
def download_receipt_pdf(request, payment_id):
    if request.user.role == 'STUDENT':
        payment = get_object_or_404(Payment, id=payment_id, student__user=request.user, status='VERIFIED')
    else:
        payment = get_object_or_404(Payment, id=payment_id, status='VERIFIED')
        
    pdf_data = generate_receipt_pdf(payment)
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Kuitansi-{payment.invoice.invoice_number}.pdf"'
    return response
