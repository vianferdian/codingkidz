from django.contrib import admin
from .models import Invoice, Payment, AdminBankAccount

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'student', 'course', 'amount', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('invoice_number', 'student__user__first_name', 'student__user__last_name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'student', 'amount', 'payment_method', 'status', 'paid_at', 'verified_by')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('invoice__invoice_number', 'student__user__first_name', 'student__user__last_name')

@admin.register(AdminBankAccount)
class AdminBankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_number', 'account_name', 'status')
    list_filter = ('status',)
    search_fields = ('bank_name', 'account_number', 'account_name')

