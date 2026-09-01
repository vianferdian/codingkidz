from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('invoices/', views.student_invoice_list, name='student_invoice_list'),
    path('pay/<int:invoice_id>/', views.student_pay_invoice, name='student_pay_invoice'),
    path('verification/', views.admin_payment_verification, name='admin_payment_verification'),
    path('verify/<int:payment_id>/', views.admin_verify_payment, name='admin_verify_payment'),
    path('trigger-billing/', views.admin_trigger_billing, name='admin_trigger_billing'),
    
    # Custom Admin Invoices
    path('admin-invoices/', views.admin_invoice_list, name='admin_invoice_list'),
    path('admin-invoices/add/', views.admin_add_invoice, name='admin_add_invoice'),
    path('admin-invoices/<int:invoice_id>/edit/', views.admin_edit_invoice, name='admin_edit_invoice'),
    
    # Custom Admin Cash Payments
    path('admin-payments/', views.admin_payment_list, name='admin_payment_list'),
    path('admin-payments/record-cash/', views.admin_record_cash_payment, name='admin_record_cash_payment'),
    
    # Custom Bank Accounts
    path('bank-accounts/', views.admin_bank_account_list, name='admin_bank_account_list'),
    path('bank-accounts/add/', views.admin_add_bank_account, name='admin_add_bank_account'),
    path('bank-accounts/<int:account_id>/edit/', views.admin_edit_bank_account, name='admin_edit_bank_account'),
    path('bank-accounts/<int:account_id>/delete/', views.admin_delete_bank_account, name='admin_delete_bank_account'),
    
    # Custom Admin QRIS Settings
    path('qris/', views.admin_qris_list, name='admin_qris_list'),
    path('qris/add/', views.admin_add_qris, name='admin_add_qris'),
    path('qris/<int:qris_id>/edit/', views.admin_edit_qris, name='admin_edit_qris'),
    path('qris/<int:qris_id>/delete/', views.admin_delete_qris, name='admin_delete_qris'),
    
    # PDF Downloads
    path('invoice/<int:invoice_id>/download/', views.download_invoice_pdf, name='download_invoice_pdf'),
    path('receipt/<int:payment_id>/download/', views.download_receipt_pdf, name='download_receipt_pdf'),
]
