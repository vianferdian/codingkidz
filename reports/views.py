import io
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from django.db.models import Sum

# Import models dari apps lain
from students.models import Student
from attendance.models import Attendance
from payments.models import Payment, Invoice
from projects.models import ProjectSubmission

# ReportLab Imports
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os
from django.conf import settings
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

def format_rupiah(amount):
    if amount is None:
        return "Rp 0"
    return f"Rp {int(amount):,}".replace(',', '.')

def generate_pdf_report(filename, title, headers, data, col_widths=None, extra_info=None):
    """
    Helper function untuk membuat file PDF laporan standar menggunakan ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    elements = []
    styles = getSampleStyleSheet()

    header_cell_style = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=TA_LEFT
    )

    body_cell_style = ParagraphStyle(
        'BodyCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#334155'),
        alignment=TA_LEFT
    )

    # Brand Logo & Title Header
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'getskills', 'images', 'gamepad.png')
    brand_text = Paragraph('<font size="16" color="#e11d48"><b>Neper</b></font><font size="16" color="#0f172a"><b>CodingKidz</b></font><br/><font size="8" color="#64748B">Kursus Coding Anak & Remaja</font>', styles['Normal'])
    
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=32, height=32)
        brand_cell = Table([[logo_img, brand_text]], colWidths=[38, 250])
        brand_cell.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 0),
        ]))
    else:
        brand_cell = brand_text

    today_str = datetime.now().strftime("%d-%m-%Y %H:%M")
    right_text = f"<b>{title.upper()}</b><br/><font size='8.5' color='#64748B'>Tanggal Dicetak: {today_str}"
    if extra_info:
        right_text += f" | {extra_info}"
    right_text += "</font>"
    
    right_p = Paragraph(right_text, ParagraphStyle('HeaderRight', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=13, leading=16, fontName='Helvetica-Bold', textColor=colors.HexColor('#1E293B')))

    header_table = Table([[brand_cell, right_p]], colWidths=[320, 449.89])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('PADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#e11d48'), spaceAfter=14))

    # Format Header Tabel
    table_data = []
    header_row = [Paragraph(f"<b>{h}</b>", header_cell_style) for h in headers]
    table_data.append(header_row)

    # Format Data Rows
    for row in data:
        formatted_row = []
        for cell in row:
            text = str(cell) if cell is not None else "-"
            formatted_row.append(Paragraph(text, body_cell_style))
        table_data.append(formatted_row)

    # Hitung lebar kolom otomatis jika tidak ditentukan
    page_width = 841.89 - 72  # 769.89 pt available width
    if not col_widths:
        num_cols = len(headers)
        col_widths = [page_width / num_cols] * num_cols

    # Table Styling
    t = Table(table_data, colWidths=col_widths, repeatRows=1)
    t_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]

    for i in range(1, len(table_data)):
        if i % 2 == 0:
            t_style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8FAFC')))
        else:
            t_style.append(('BACKGROUND', (0, i), (-1, i), colors.white))

    t.setStyle(TableStyle(t_style))
    elements.append(t)

    # Build PDF Document
    doc.build(elements)
    
    pdf_val = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}.pdf"'
    response.write(pdf_val)
    return response


@login_required(login_url='getskills:login')
@role_required(allowed_roles=['ADMIN'])
def student_report(request):
    students = Student.objects.all().select_related('user').order_by('-id')
    context = {
        "page_title": "Laporan Data Siswa",
        "students": students
    }
    return render(request, 'reports/student_report.html', context)


@login_required(login_url='getskills:login')
@role_required(allowed_roles=['ADMIN'])
def student_report_pdf(request):
    students = Student.objects.all().select_related('user').order_by('-id')
    headers = ['Kode Siswa', 'Nama Lengkap', 'Email', 'Sekolah', 'Nama Wali', 'No. Telp Wali', 'Status']
    col_widths = [80, 130, 150, 110, 110, 110, 79.89]
    data = []
    for s in students:
        full_name = f"{s.user.first_name} {s.user.last_name}".strip() or s.user.username
        status_text = "Aktif" if s.status == 'ACTIVE' else s.status
        data.append([
            s.student_code,
            full_name,
            s.user.email,
            s.school_name or "-",
            s.parent_name or "-",
            s.parent_phone or "-",
            status_text
        ])
    return generate_pdf_report(
        filename=f"Laporan_Siswa_{datetime.now().strftime('%Y%m%d')}",
        title="Laporan Data Siswa",
        headers=headers,
        data=data,
        col_widths=col_widths
    )


@login_required(login_url='getskills:login')
@role_required(allowed_roles=['ADMIN'])
def attendance_report(request):
    attendances = Attendance.objects.all().select_related('student__user', 'course_session__course').order_by('-check_in_at', '-id')
    context = {
        "page_title": "Laporan Kehadiran Siswa",
        "attendances": attendances
    }
    return render(request, 'reports/attendance_report.html', context)


@login_required(login_url='getskills:login')
@role_required(allowed_roles=['ADMIN'])
def attendance_report_pdf(request):
    attendances = Attendance.objects.all().select_related('student__user', 'course_session__course').order_by('-check_in_at', '-id')
    headers = ['Tanggal', 'Nama Siswa', 'Kelas', 'Sesi / Pertemuan', 'Status Kehadiran', 'Catatan']
    col_widths = [90, 140, 140, 150, 90, 159.89]
    data = []
    for att in attendances:
        dt_str = att.check_in_at.strftime("%d-%m-%Y %H:%M") if att.check_in_at else "-"
        student_name = f"{att.student.user.first_name} {att.student.user.last_name}".strip() if att.student and att.student.user else "-"
        course_name = att.course_session.course.name if att.course_session and att.course_session.course else "-"
        session_info = f"{att.course_session.title or '-'} (Sesi #{att.course_session.session_number})" if att.course_session else "-"
        status_text = att.status.title() if att.status else "-"
        notes = att.notes or "-"
        data.append([
            dt_str,
            student_name,
            course_name,
            session_info,
            status_text,
            notes
        ])
    return generate_pdf_report(
        filename=f"Laporan_Kehadiran_{datetime.now().strftime('%Y%m%d')}",
        title="Laporan Kehadiran Siswa",
        headers=headers,
        data=data,
        col_widths=col_widths
    )


@login_required(login_url='getskills:login')
@role_required(allowed_roles=['ADMIN'])
def payment_report(request):
    payments = Payment.objects.all().select_related('invoice__student__user').order_by('-paid_at')
    context = {
        "page_title": "Laporan Pembayaran Siswa",
        "payments": payments
    }
    return render(request, 'reports/payment_report.html', context)


@login_required(login_url='getskills:login')
@role_required(allowed_roles=['ADMIN'])
def payment_report_pdf(request):
    payments = Payment.objects.all().select_related('invoice__student__user').order_by('-paid_at')
    headers = ['ID Tagihan', 'Nama Siswa', 'Jumlah Bayar', 'Metode Pembayaran', 'Tanggal Transfer', 'Status Verifikasi']
    col_widths = [80, 170, 110, 120, 130, 159.89]
    data = []
    for p in payments:
        inv_id = f"#{p.invoice.id}" if p.invoice else "-"
        student_name = f"{p.invoice.student.user.first_name} {p.invoice.student.user.last_name}".strip() if p.invoice and p.invoice.student and p.invoice.student.user else "-"
        method = "Cash" if p.payment_method == 'CASH' else "Transfer Bank"
        paid_dt = p.paid_at.strftime("%d-%m-%Y %H:%M") if p.paid_at else "-"
        status_map = {'VERIFIED': 'Terverifikasi', 'PENDING': 'Menunggu'}
        status_text = status_map.get(p.status, p.status)
        data.append([
            inv_id,
            student_name,
            format_rupiah(p.amount),
            method,
            paid_dt,
            status_text
        ])
    return generate_pdf_report(
        filename=f"Laporan_Pembayaran_{datetime.now().strftime('%Y%m%d')}",
        title="Laporan Pembayaran Siswa",
        headers=headers,
        data=data,
        col_widths=col_widths
    )


@login_required(login_url='getskills:login')
@role_required(allowed_roles=['ADMIN'])
def project_report(request):
    submissions = ProjectSubmission.objects.all().select_related('student__user', 'project__course').order_by('-submitted_at')
    context = {
        "page_title": "Laporan Pengumpulan Project",
        "submissions": submissions
    }
    return render(request, 'reports/project_report.html', context)


@login_required(login_url='getskills:login')
@role_required(allowed_roles=['ADMIN'])
def project_report_pdf(request):
    submissions = ProjectSubmission.objects.all().select_related('student__user', 'project__course').order_by('-submitted_at')
    headers = ['Tanggal', 'Nama Siswa', 'Judul Project', 'Program / Kelas', 'Nilai', 'Status', 'Umpan Balik']
    col_widths = [80, 130, 140, 130, 60, 90, 139.89]
    data = []
    for sub in submissions:
        sub_dt = sub.submitted_at.strftime("%d-%m-%Y") if sub.submitted_at else "-"
        student_name = f"{sub.student.user.first_name} {sub.student.user.last_name}".strip() if sub.student and sub.student.user else "-"
        proj_title = sub.project.title if sub.project else "-"
        course_name = sub.project.course.name if sub.project and sub.project.course else "-"
        score = str(sub.score) if sub.score is not None else "-"
        status_map = {'COMPLETED': 'Completed', 'REVISION_REQUIRED': 'Revisi'}
        status_text = status_map.get(sub.status, sub.status.title() if sub.status else "-")
        feedback = sub.feedback or "-"
        data.append([
            sub_dt,
            student_name,
            proj_title,
            course_name,
            score,
            status_text,
            feedback
        ])
    return generate_pdf_report(
        filename=f"Laporan_Project_{datetime.now().strftime('%Y%m%d')}",
        title="Laporan Pengumpulan Project",
        headers=headers,
        data=data,
        col_widths=col_widths
    )


@login_required(login_url='getskills:login')
@role_required(allowed_roles=['ADMIN'])
def revenue_report(request):
    paid_invoices = Invoice.objects.filter(status='PAID').select_related('student__user').order_by('-due_date')
    total_revenue = Payment.objects.filter(status='VERIFIED').aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        "page_title": "Laporan Pendapatan Les",
        "paid_invoices": paid_invoices,
        "total_revenue": total_revenue
    }
    return render(request, 'reports/revenue_report.html', context)


@login_required(login_url='getskills:login')
@role_required(allowed_roles=['ADMIN'])
def revenue_report_pdf(request):
    paid_invoices = Invoice.objects.filter(status='PAID').select_related('student__user').order_by('-due_date')
    total_revenue = Payment.objects.filter(status='VERIFIED').aggregate(total=Sum('amount'))['total'] or 0
    headers = ['No. Invoice', 'Nama Siswa', 'Jumlah Tagihan', 'Deskripsi', 'Tanggal Jatuh Tempo', 'Status']
    col_widths = [90, 160, 120, 180, 110, 109.89]
    data = []
    for inv in paid_invoices:
        inv_id = f"#{inv.id}"
        student_name = f"{inv.student.user.first_name} {inv.student.user.last_name}".strip() if inv.student and inv.student.user else "-"
        due_dt = inv.due_date.strftime("%d-%m-%Y") if inv.due_date else "-"
        course_desc = inv.course.name if inv.course else "Tagihan Les"
        data.append([
            inv_id,
            student_name,
            format_rupiah(inv.amount),
            course_desc,
            due_dt,
            "Lunas / Paid"
        ])
    return generate_pdf_report(
        filename=f"Laporan_Pendapatan_{datetime.now().strftime('%Y%m%d')}",
        title="Laporan Pendapatan Les",
        headers=headers,
        data=data,
        col_widths=col_widths,
        extra_info=f"Total Terverifikasi: {format_rupiah(total_revenue)}"
    )
