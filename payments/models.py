from django.db import models
from django.conf import settings
from students.models import Student
from academics.models import Course, CourseSession

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    invoice_number = models.CharField(max_length=100, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='invoices')
    course_session = models.ForeignKey(CourseSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNPAID')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.invoice_number} - {self.status}"

class Payment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending Verification'),
        ('VERIFIED', 'Verified (Paid)'),
        ('FAILED', 'Failed / Rejected'),
    )
    METHOD_CHOICES = (
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('QRIS', 'QRIS'),
        ('GATEWAY', 'Payment Gateway (Midtrans/Qris/etc)'),
    )
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=METHOD_CHOICES, default='CASH')
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    paid_at = models.DateTimeField(blank=True, null=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payments')
    verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.invoice.invoice_number} - {self.status}"


class AdminBankAccount(models.Model):
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=150)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number} ({self.account_name})"


class AdminQrisSetting(models.Model):
    name = models.CharField(max_length=100, default="QRIS Pembayaran Official")
    qris_image = models.ImageField(upload_to='qris_images/')
    notes = models.TextField(blank=True, null=True, help_text="Catatan atau petunjuk pembayaran QRIS")
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({'Aktif' if self.status else 'Nonaktif'})"


