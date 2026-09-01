from django import forms
from django.utils import timezone
from .models import Invoice, Payment, AdminBankAccount, AdminQrisSetting

class AdminQrisForm(forms.ModelForm):
    class Meta:
        model = AdminQrisSetting
        fields = [
            'name',
            'qris_image',
            'notes',
            'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama QRIS (Contoh: QRIS BCA / All Payment)'}),
            'qris_image': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Petunjuk/Catatan singkat'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Nama / Label QRIS',
            'qris_image': 'Gambar QR Code QRIS',
            'notes': 'Catatan Pembayaran',
            'status': 'Status Aktif',
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'invoice_number',
            'student',
            'course',
            'amount',
            'due_date',
            'status'
        ]
        widgets = {
            'invoice_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Auto-generated jika dikosongkan'}),
            'student': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'course': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Biaya Kursus'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control default-select wide'}),
        }
        labels = {
            'invoice_number': 'Nomor Invoice',
            'student': 'Siswa',
            'course': 'Program Les / Kelas',
            'amount': 'Jumlah Tagihan',
            'due_date': 'Jatuh Tempo',
            'status': 'Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice_number'].required = False
        if not self.instance.pk and not self.initial.get('invoice_number'):
            import random
            now = timezone.now()
            self.initial['invoice_number'] = f"INV-{now.strftime('%Y%m%d-%H%M%S')}-{random.randint(10, 99)}"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.invoice_number:
            import random
            now = timezone.now()
            instance.invoice_number = f"INV-{now.strftime('%Y%m%d-%H%M%S')}-{random.randint(10, 99)}"
        if commit:
            instance.save()
        return instance


class CashPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'invoice',
            'student',
            'amount',
            'payment_reference',
            'paid_at'
        ]
        widgets = {
            'invoice': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'student': forms.Select(attrs={'class': 'form-control default-select wide'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Jumlah Diterima'}),
            'payment_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keterangan Cash (Nama Penerima / dll)'}),
            'paid_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
        labels = {
            'invoice': 'Nomor Invoice',
            'student': 'Siswa',
            'amount': 'Jumlah Pembayaran',
            'payment_reference': 'Referensi / Keterangan',
            'paid_at': 'Tanggal Pembayaran',
        }


class AdminBankAccountForm(forms.ModelForm):
    class Meta:
        model = AdminBankAccount
        fields = [
            'bank_name',
            'account_number',
            'account_name',
            'status'
        ]
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: BANK BCA, BANK MANDIRI'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nomor Rekening'}),
            'account_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Pemilik Rekening'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'bank_name': 'Nama Bank',
            'account_number': 'Nomor Rekening',
            'account_name': 'Nama Pemilik',
            'status': 'Aktif / Digunakan',
        }
