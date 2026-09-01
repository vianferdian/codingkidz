import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from academics.models import CourseEnrollment
from payments.models import Invoice

class Command(BaseCommand):
    help = 'Generate monthly invoices for all active student enrollments on the 1st of the month.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        year = today.year
        month = today.month
        month_str = today.strftime('%m')
        
        # Get all active enrollments
        active_enrollments = CourseEnrollment.objects.filter(status='ACTIVE')
        created_count = 0
        skipped_count = 0
        
        for enrollment in active_enrollments:
            student = enrollment.student
            course = enrollment.course
            
            # Formulate unique invoice number for this student, course, and month
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
            from notifications.utils import create_notification
            create_notification(
                user=student.user,
                title="Tagihan Pembayaran Baru",
                message=f"Tagihan baru {invoice.invoice_number} sebesar Rp {invoice.amount} telah diterbitkan untuk program {course.name}. Jatuh tempo: {due_date.strftime('%d-%m-%Y')}.",
                notification_type='PAYMENT'
            )
            created_count += 1
            
        self.stdout.write(self.style.SUCCESS(
            f"Proses tagihan bulanan selesai. Berhasil membuat {created_count} invoice baru. {skipped_count} invoice dilewati (sudah ada)."
        ))
