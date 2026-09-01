import os
from io import BytesIO
import datetime
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def get_brand_header_cell(styles):
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'getskills', 'images', 'gamepad.png')
    brand_p = Paragraph('<font size="14" color="#e11d48"><b>Neper</b></font><font size="14" color="#0f172a"><b>CodingKidz</b></font><br/><font size="8.5" color="#64748B">Kursus Coding Anak & Remaja<br/>Email: info@nepercodingkidz.com</font>', styles['Normal'])
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=28, height=28)
        brand_table = Table([[logo_img, brand_p]], colWidths=[34, 250])
        brand_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 0),
        ]))
        return brand_table
    return brand_p

def generate_invoice_pdf(invoice):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    
    normal_style = ParagraphStyle(
        'InvoiceNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14
    )
    bold_style = ParagraphStyle(
        'InvoiceBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14
    )
    
    # Header Table with Logo & Brand
    brand_cell = get_brand_header_cell(styles)
    header_data = [
        [
            brand_cell,
            Paragraph("<b>INVOICE</b><br/>No: " + invoice.invoice_number + "<br/>Tanggal: " + invoice.created_at.strftime('%d-%m-%Y'), bold_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[300, 240])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 20))
    
    # Bill To / Details
    student = invoice.student
    user = student.user
    details_data = [
        [
            Paragraph("<b>DITAGIHKAN KEPADA:</b><br/>Nama: " + user.first_name + " " + user.last_name + "<br/>Kode Siswa: " + student.student_code + "<br/>Orang Tua: " + (student.parent_name or "-"), normal_style),
            Paragraph("<b>RINCIAN PEMBAYARAN:</b><br/>Program: " + (invoice.course.name if invoice.course else "-") + "<br/>Jatuh Tempo: " + invoice.due_date.strftime('%d-%m-%Y') + "<br/>Status: <b>" + invoice.status + "</b>", normal_style)
        ]
    ]
    details_table = Table(details_data, colWidths=[270, 270])
    details_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8F9FA')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 20))
    
    # Items Table
    items_data = [
        [Paragraph("<font color='white'><b>Deskripsi Layanan / Program</b></font>", bold_style), Paragraph("<font color='white'><b>Jumlah</b></font>", bold_style)]
    ]
    desc = f"Biaya Kursus Coding - Program: {invoice.course.name if invoice.course else '-'}"
    if invoice.course_session:
        desc += f" (Sesi #{invoice.course_session.session_number})"
    items_data.append([
        Paragraph(desc, normal_style),
        Paragraph(f"Rp {invoice.amount:,.2f}", normal_style)
    ])
    
    items_data.append([
        Paragraph("<b>Total Tagihan</b>", bold_style),
        Paragraph(f"<b>Rp {invoice.amount:,.2f}</b>", bold_style)
    ])
    
    items_table = Table(items_data, colWidths=[400, 140])
    items_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DEE2E6')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#374557')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 30))
    
    # Footer Note
    story.append(Paragraph("<b>Catatan Transfer Bank / QRIS:</b><br/>Silakan lakukan pembayaran sebelum tanggal jatuh tempo.<br/>Pembayaran dapat dilakukan melalui Transfer Bank atau QRIS resmi yang tertera pada menu Pembayaran dashboard Anda.", normal_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<font color='#6C757D'>Terima kasih atas kepercayaan Anda belajar coding bersama Neper CodingKidz!</font>", normal_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_receipt_pdf(payment):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    
    normal_style = ParagraphStyle(
        'ReceiptNormal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14
    )
    bold_style = ParagraphStyle(
        'ReceiptBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14
    )
    
    # Header Table with Logo & Brand
    brand_cell = get_brand_header_cell(styles)
    header_data = [
        [
            brand_cell,
            Paragraph("<b>KUITANSI / BUKTI BAYAR</b><br/>No. Invoice: " + payment.invoice.invoice_number + "<br/>Tanggal Bayar: " + (payment.paid_at.strftime('%d-%m-%Y %H:%M') if payment.paid_at else "-"), bold_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[300, 240])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 20))
    
    # Details
    student = payment.student
    user = student.user
    details_data = [
        [
            Paragraph("<b>TELAH DITERIMA DARI:</b><br/>Nama: " + user.first_name + " " + user.last_name + "<br/>Kode Siswa: " + student.student_code, normal_style),
            Paragraph("<b>RINCIAN TRANSAKSI:</b><br/>Metode: " + payment.get_payment_method_display() + "<br/>Ref/Pengirim: " + (payment.payment_reference or "-") + "<br/>Status: <b>LUNAS / VERIFIED</b>", normal_style)
        ]
    ]
    details_table = Table(details_data, colWidths=[270, 270])
    details_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#E9F7EF')),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 20))
    
    # Items Table
    items_data = [
        [Paragraph("<font color='white'><b>Deskripsi Pembayaran</b></font>", bold_style), Paragraph("<font color='white'><b>Jumlah Bayar</b></font>", bold_style)]
    ]
    desc = f"Pembayaran Biaya Kursus - Program: {payment.invoice.course.name if payment.invoice.course else '-'}"
    if payment.invoice.course_session:
        desc += f" (Sesi #{payment.invoice.course_session.session_number})"
    items_data.append([
        Paragraph(desc, normal_style),
        Paragraph(f"Rp {payment.amount:,.2f}", normal_style)
    ])
    items_data.append([
        Paragraph("<b>Total Pembayaran</b>", bold_style),
        Paragraph(f"<b>Rp {payment.amount:,.2f}</b>", bold_style)
    ])
    
    items_table = Table(items_data, colWidths=[400, 140])
    items_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DEE2E6')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#28A745')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (1,1), (1,-1), 'RIGHT'),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 30))
    
    # Signature/Approval
    sig_data = [
        [
            Paragraph("", normal_style),
            Paragraph("Diverifikasi Oleh:<br/><br/><br/><b>" + (payment.verified_by.first_name + " " + payment.verified_by.last_name if payment.verified_by else "Sistem") + "</b><br/>Staf Neper CodingKidz", normal_style)
        ]
    ]
    sig_table = Table(sig_data, colWidths=[360, 180])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
    ]))
    story.append(sig_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
