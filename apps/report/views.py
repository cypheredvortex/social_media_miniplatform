from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from bson import ObjectId

from .models import Report
from apps.user.models import User
from apps.enums.models import ReportStatus

# ---------------------------
# Admin Report Views
# ---------------------------

# List all reports
def admin_report_list(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'admin/admin_report_list.html', {'reports': reports})


# View report details
def admin_report_detail(request, report_id):
    try:
        obj_id = ObjectId(report_id)
    except Exception:
        raise Http404("Invalid report ID")

    report = get_object_or_404(Report, id=obj_id)
    return render(request, 'admin/report_detail.html', {'report': report})


# Resolve a report
def admin_report_resolve(request, report_id):
    try:
        obj_id = ObjectId(report_id)
    except Exception:
        raise Http404("Invalid report ID")

    report = get_object_or_404(Report, id=obj_id)
    report.resolve()
    messages.success(request, 'Report resolved successfully.')
    return redirect('report:admin_report_list')


# Reject a report
def admin_report_reject(request, report_id):
    try:
        obj_id = ObjectId(report_id)
    except Exception:
        raise Http404("Invalid report ID")

    report = get_object_or_404(Report, id=obj_id)
    report.reject()
    messages.success(request, 'Report rejected successfully.')
    return redirect('report:admin_report_list')


# Send warning to a user (linked to a report or independent)
def admin_send_warning(request, user_id):
    try:
        obj_id = ObjectId(user_id)
    except Exception:
        raise Http404("Invalid user ID")

    user = get_object_or_404(User, id=obj_id)

    # Example: increment warning count on user
    if hasattr(user, 'warning_count'):
        user.warning_count += 1
    else:
        user.warning_count = 1
    user.save()

    # Optional: email warning
    # from django.core.mail import send_mail
    # send_mail(
    #     'Warning Notification',
    #     'You have received a warning due to reported content. Please adhere to the platform rules.',
    #     'admin@example.com',
    #     [user.email],
    #     fail_silently=True,
    # )

    messages.success(request, f'Warning sent to {user.username}.')
    return redirect('report:admin_report_list')
