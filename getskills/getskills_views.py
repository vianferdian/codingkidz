from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from students.models import Student
from tutors.models import Teacher
from academics.models import Course, CourseSession, CourseEnrollment
from attendance.models import Attendance
from payments.models import Invoice, Payment
from projects.models import Project, ProjectSubmission


@login_required(login_url='getskills:login')
def index(request):
    role = request.user.role
    context = {
        "page_title": "Dashboard",
        "role": role,
    }
    
    if role == 'ADMIN':
        # Admin statistics
        context.update({
            "total_students": Student.objects.count(),
            "total_tutors": Teacher.objects.filter(type='TUTOR').count(),
            "total_teachers": Teacher.objects.filter(type='GURU').count(),
            "total_courses": Course.objects.count(),
            "unpaid_invoices": Invoice.objects.filter(status='UNPAID').count(),
            "total_revenue": Payment.objects.filter(status='VERIFIED').aggregate(total=Sum('amount'))['total'] or 0,
            "pending_projects": ProjectSubmission.objects.filter(status='SUBMITTED').count(),
        })
        return render(request, 'getskills/index.html', context)
        
    elif role == 'TUTOR':
        # Tutor statistics
        try:
            teacher_profile = request.user.teacher_profile
            my_sessions = CourseSession.objects.filter(teacher=teacher_profile)
            my_courses = Course.objects.filter(sessions__teacher=teacher_profile).distinct()
            my_students_count = Student.objects.filter(enrollments__course__in=my_courses).distinct().count()
            pending_review = ProjectSubmission.objects.filter(project__course__in=my_courses, status='SUBMITTED').count()
            
            context.update({
                "my_classes_count": my_courses.count(),
                "my_students_count": my_students_count,
                "pending_review_count": pending_review,
                "my_sessions": my_sessions[:5],
            })
        except Teacher.DoesNotExist:
            context.update({
                "my_classes_count": 0,
                "my_students_count": 0,
                "pending_review_count": 0,
                "my_sessions": [],
            })
        return render(request, 'getskills/index.html', context)

        
    elif role == 'STUDENT':
        # Student statistics
        try:
            student_profile = request.user.student_profile
            my_enrollments = CourseEnrollment.objects.filter(student=student_profile)
            my_courses = Course.objects.filter(enrollments__student=student_profile)
            unpaid_invoices_count = Invoice.objects.filter(student=student_profile, status='UNPAID').count()
            active_projects_count = Project.objects.filter(course__in=my_courses, status='ACTIVE').count()
            
            # Attendance percentage
            total_attendance = Attendance.objects.filter(student=student_profile).count()
            present_attendance = Attendance.objects.filter(student=student_profile, status='HADIR').count()
            attendance_rate = int((present_attendance / total_attendance) * 100) if total_attendance > 0 else 100
            
            context.update({
                "active_classes_count": my_courses.filter(status='ACTIVE').count(),
                "unpaid_invoices_count": unpaid_invoices_count,
                "active_projects_count": active_projects_count,
                "attendance_rate": attendance_rate,
            })
        except Student.DoesNotExist:
            context.update({
                "active_classes_count": 0,
                "unpaid_invoices_count": 0,
                "active_projects_count": 0,
                "attendance_rate": 100,
            })
        return render(request, 'getskills/index.html', context)
        
    return render(request, 'getskills/index.html', context)

@login_required(login_url='getskills:login')
def index2(request):
    context={
        "page_title":"Dashboard"
    }
    return render(request,'getskills/index-2.html',context)

@login_required(login_url='getskills:login')
def schedule(request):
    context={
        "page_title":"Schedule"
    }
    return render(request,'getskills/schedule.html',context)

@login_required(login_url='getskills:login')
def instructors(request):
    context={
        "page_title":"Instructors"
    }
    return render(request,'getskills/instructors.html',context)

@login_required(login_url='getskills:login')
def message(request):
    context={
        "page_title":"Message"
    }
    return render(request,'getskills/message.html',context)

@login_required(login_url='getskills:login')
def activity(request):
    context={
        "page_title":"Activity"
    }
    return render(request,'getskills/activity.html',context)

@login_required(login_url='getskills:login')
def profile(request):
    context={
        "page_title":"Profile"
    }
    return render(request,'getskills/profile.html',context)

@login_required(login_url='getskills:login')
def courses(request):
    context={
        "page_title":"Courses"
    }
    return render(request,'getskills/courses/courses.html',context)


@login_required(login_url='getskills:login')
def course_details_1(request):
    context={
        "page_title":"Courses"
    }
    return render(request,'getskills/courses/course-details-1.html',context)

@login_required(login_url='getskills:login')
def course_details_2(request):
    context={
        "page_title":"Courses"
    }
    return render(request,'getskills/courses/course-details-2.html',context)

@login_required(login_url='getskills:login')
def instructor_dashboard(request):
    context={
        "page_title":"Dashboard"
    }
    return render(request,'getskills/instructor/instructor-dashboard.html',context)

@login_required(login_url='getskills:login')
def instructor_courses(request):
    context={
        "page_title":"Courses"
    }
    return render(request,'getskills/instructor/instructor-courses.html',context)

@login_required(login_url='getskills:login')
def instructor_schedule(request):
    context={
        "page_title":"Instructor Schedule"
    }
    return render(request,'getskills/instructor/instructor-schedule.html',context)

@login_required(login_url='getskills:login')
def instructor_students(request):
    context={
        "page_title":"Instructor Students"
    }
    return render(request,'getskills/instructor/instructor-students.html',context)

@login_required(login_url='getskills:login')
def instructor_resources(request):
    context={
        "page_title":"Instructor Resources"
    }
    return render(request,'getskills/instructor/instructor-resources.html',context)

@login_required(login_url='getskills:login')
def instructor_transactions(request):
    context={
        "page_title":"Instructor Transactions"
    }
    return render(request,'getskills/instructor/instructor-transactions.html',context)

@login_required(login_url='getskills:login')
def instructor_liveclass(request):
    context={
        "page_title":"Live Class"
    }
    return render(request,'getskills/instructor/instructor-liveclass.html',context)

@login_required(login_url='getskills:login')
def app_profile(request):
    context={
        "page_title":"Profile"
    }
    return render(request,'getskills/apps/app-profile.html',context)

@login_required(login_url='getskills:login')
def post_details(request):
    context={
        "page_title":"Post Details"
    }
    return render(request,'getskills/apps/post-details.html',context)

@login_required(login_url='getskills:login')
def email_compose(request):
    context={
        "page_title":"Compose"
    }
    return render(request,'getskills/apps/email/email-compose.html',context)

@login_required(login_url='getskills:login')
def email_inbox(request):
    context={
        "page_title":"Inbox"
    }
    return render(request,'getskills/apps/email/email-inbox.html',context)

@login_required(login_url='getskills:login')
def email_read(request):
    context={
        "page_title":"Read"
    }
    return render(request,'getskills/apps/email/email-read.html',context)

@login_required(login_url='getskills:login')
def app_calender(request):
    context={
        "page_title":"Calendar"
    }
    return render(request,'getskills/apps/app-calender.html',context)

@login_required(login_url='getskills:login')
def ecom_product_grid(request):
    context={
        "page_title":"Product-Grid"
    }
    return render(request,'getskills/apps/shop/ecom-product-grid.html',context)

@login_required(login_url='getskills:login')
def ecom_product_list(request):
    context={
        "page_title":"Product-List"
    }
    return render(request,'getskills/apps/shop/ecom-product-list.html',context)

@login_required(login_url='getskills:login')
def ecom_product_detail(request):
    context={
        "page_title":"Product-Detail"
    }
    return render(request,'getskills/apps/shop/ecom-product-detail.html',context)

@login_required(login_url='getskills:login')
def ecom_product_order(request):
    context={
        "page_title":"Product-Order"
    }
    return render(request,'getskills/apps/shop/ecom-product-order.html',context)

@login_required(login_url='getskills:login')
def ecom_checkout(request):
    context={
        "page_title":"Checkout"
    }
    return render(request,'getskills/apps/shop/ecom-checkout.html',context)

@login_required(login_url='getskills:login')
def ecom_invoice(request):
    context={
        "page_title":"Invoice"
    }
    return render(request,'getskills/apps/shop/ecom-invoice.html',context)

@login_required(login_url='getskills:login')
def ecom_customers(request):
    context={
        "page_title":"Customers"
    }
    return render(request,'getskills/apps/shop/ecom-customers.html',context)

@login_required(login_url='getskills:login')
def chart_flot(request):
    context={
        "page_title":"Chart-Flot"
    }
    return render(request,'getskills/charts/chart-flot.html',context)

@login_required(login_url='getskills:login')
def chart_morris(request):
    context={
        "page_title":"Chart-Morris"
    }
    return render(request,'getskills/charts/chart-morris.html',context)

@login_required(login_url='getskills:login')
def chart_chartjs(request):
    context={
        "page_title":"Chart-Chartjs"
    }
    return render(request,'getskills/charts/chart-chartjs.html',context)

@login_required(login_url='getskills:login')
def chart_chartist(request):
    context={
        "page_title":"Chart-Chartist"
    }
    return render(request,'getskills/charts/chart-chartist.html',context)

@login_required(login_url='getskills:login')
def chart_sparkline(request):
    context={
        "page_title":"Chart-Sparkline"
    }
    return render(request,'getskills/charts/chart-sparkline.html',context)

@login_required(login_url='getskills:login')
def chart_peity(request):
    context={
        "page_title":"Chart-Peity"
    }
    return render(request,'getskills/charts/chart-peity.html',context)

@login_required(login_url='getskills:login')
def ui_accordion(request):
    context={
        "page_title":"Accordion"
    }
    return render(request,'getskills/bootstrap/ui-accordion.html',context)

@login_required(login_url='getskills:login')
def ui_alert(request):
    context={
        "page_title":"Alert"
    }
    return render(request,'getskills/bootstrap/ui-alert.html',context)

@login_required(login_url='getskills:login')  
def ui_badge(request):
    context={
        "page_title":"Badge"
    }
    return render(request,'getskills/bootstrap/ui-badge.html',context)

@login_required(login_url='getskills:login')
def ui_button(request):
    context={
        "page_title":"Button"
    }
    return render(request,'getskills/bootstrap/ui-button.html',context)

@login_required(login_url='getskills:login')
def ui_modal(request):
    context={
        "page_title":"Modal"
    }
    return render(request,'getskills/bootstrap/ui-modal.html',context)

@login_required(login_url='getskills:login')
def ui_button_group(request):
    context={
        "page_title":"Button Group"
    }
    return render(request,'getskills/bootstrap/ui-button-group.html',context)

@login_required(login_url='getskills:login')
def ui_list_group(request):
    context={
        "page_title":"List Group"
    }
    return render(request,'getskills/bootstrap/ui-list-group.html',context)

@login_required(login_url='getskills:login')
def ui_media_object(request):
    context={
        "page_title":"Media Object"
    }
    return render(request,'getskills/bootstrap/ui-media-object.html',context)

@login_required(login_url='getskills:login')
def ui_card(request):
    context={
        "page_title":"Card"
    }
    return render(request,'getskills/bootstrap/ui-card.html',context)

@login_required(login_url='getskills:login')
def ui_carousel(request):
    context={
        "page_title":"Carousel"
    }
    return render(request,'getskills/bootstrap/ui-carousel.html',context)

@login_required(login_url='getskills:login')
def ui_dropdown(request):
    context={
        "page_title":"Dropdown"
    }
    return render(request,'getskills/bootstrap/ui-dropdown.html',context)

@login_required(login_url='getskills:login')
def ui_popover(request):
    context={
        "page_title":"Popover"
    }
    return render(request,'getskills/bootstrap/ui-popover.html',context)

@login_required(login_url='getskills:login')
def ui_progressbar(request):
    context={
        "page_title":"Progressbar"
    }
    return render(request,'getskills/bootstrap/ui-progressbar.html',context)

@login_required(login_url='getskills:login')
def ui_tab(request):
    context={
        "page_title":"Tab"
    }
    return render(request,'getskills/bootstrap/ui-tab.html',context)

@login_required(login_url='getskills:login')
def ui_typography(request):
    context={
        "page_title":"Typography"
    }
    return render(request,'getskills/bootstrap/ui-typography.html',context)

@login_required(login_url='getskills:login')
def ui_pagination(request):
    context={
        "page_title":"Pagination"
    }
    return render(request,'getskills/bootstrap/ui-pagination.html',context)

@login_required(login_url='getskills:login')
def ui_grid(request):
    context={
        "page_title":"Grid"
    }
    return render(request,'getskills/bootstrap/ui-grid.html',context)

@login_required(login_url='getskills:login')
def uc_select2(request):
    context={
        "page_title":"Select"
    }
    return render(request,'getskills/plugins/uc-select2.html',context)

@login_required(login_url='getskills:login')
def uc_nestable(request):
    context={
        "page_title":"Nestable"
    }
    return render(request,'getskills/plugins/uc-nestable.html',context)

@login_required(login_url='getskills:login')
def uc_noui_slider(request):
    context={
        "page_title":"UI Slider"
    }
    return render(request,'getskills/plugins/uc-noui-slider.html',context)

@login_required(login_url='getskills:login')
def uc_sweetalert(request):
    context={
        "page_title":"Sweet Alert"
    }
    return render(request,'getskills/plugins/uc-sweetalert.html',context)

@login_required(login_url='getskills:login')
def uc_toastr(request):
    context={
        "page_title":"Toastr"
    }
    return render(request,'getskills/plugins/uc-toastr.html',context)

@login_required(login_url='getskills:login')
def map_jqvmap(request):
    context={
        "page_title":"Jqvmap"
    }
    return render(request,'getskills/plugins/map-jqvmap.html',context)

@login_required(login_url='getskills:login')
def uc_lightgallery(request):
    context={
        "page_title":"LightGallery"
    }
    return render(request,'getskills/plugins/uc-lightgallery.html',context)

@login_required(login_url='getskills:login')
def widget_basic(request):
    context={
        "page_title":"Widget"
    }
    return render(request,'getskills/widget-basic.html',context)

@login_required(login_url='getskills:login')
def form_element(request):
    context={
        "page_title":"Form Element"
    }
    return render(request,'getskills/forms/form-element.html',context)

@login_required(login_url='getskills:login')
def form_wizard(request):
    context={
        "page_title":"Form Wizard"
    }
    return render(request,'getskills/forms/form-wizard.html',context)

@login_required(login_url='getskills:login')
def form_ckeditor(request):
    context={
        "page_title":"Ckeditor"
    }
    return render(request,'getskills/forms/form-ckeditor.html',context)

@login_required(login_url='getskills:login')
def form_pickers(request):
    context={
        "page_title":"Pickers"
    }
    return render(request,'getskills/forms/form-pickers.html',context)

@login_required(login_url='getskills:login')
def form_validation(request):
    context={
        "page_title":"Form Validation"
    }
    return render(request,'getskills/forms/form-validation-jquery.html',context)


@login_required(login_url='getskills:login')
def table_bootstrap_basic(request):
    context={
        "page_title":"Table Bootstrap"
    }
    return render(request,'getskills/table/table-bootstrap-basic.html',context)

@login_required(login_url='getskills:login')
def table_datatable_basic(request):
    context={
        "page_title":"Table Datatable"
    }
    return render(request,'getskills/table/table-datatable-basic.html',context)





def page_lock_screen(request):
    return render(request,'getskills/pages/page-lock-screen.html')





def page_error_400(request):
    return render(request,'400.html')
    
def page_error_403(request):
    return render(request,'403.html')

def page_error_404(request):
    return render(request,'404.html')

def page_error_500(request):
    return render(request,'500.html')

def page_error_503(request):
    return render(request,'503.html')

def empty_page(request):
    context={
        "page_title":"Page Empty"
    }
    return render(request,'getskills/pages/empty-page.html',context)

