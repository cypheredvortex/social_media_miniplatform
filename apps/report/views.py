from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Report
from apps.user.models import User
from apps.enums.models import ReportStatus
from django.core.mail import send_mail  # optional, if sending email warnings

# List all reports
def admin_report_list(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'admin/report_list.html', {'reports': reports})


# View report details
def admin_report_detail(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    return render(request, 'admin/report_detail.html', {'report': report})


# Resolve a report
def admin_report_resolve(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.resolve()
    messages.success(request, 'Report resolved successfully.')
    return redirect('admin_report_list')


# Reject a report
def admin_report_reject(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.reject()
    messages.success(request, 'Report rejected successfully.')
    return redirect('admin_report_list')


# Send warning to a user
def admin_send_warning(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    # Example: set a warning flag on user or increment warning count
    if hasattr(user, 'warning_count'):
        user.warning_count += 1
    else:
        user.warning_count = 1
    user.save()
    
    # Optional: send email notification to user
    # send_mail(
    #     'Warning Notification',
    #     'You have received a warning due to reported content. Please adhere to the platform rules.',
    #     'admin@example.com',
    #     [user.email],
    #     fail_silently=True,
    # )
    
    messages.success(request, f'Warning sent to {user.username}.')
    return redirect('admin_report_list')
