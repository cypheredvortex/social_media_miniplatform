from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import ContentForm  # We'll create this form to handle edits
from apps.enums.models import ContentStatus
from django.shortcuts import get_object_or_404, redirect
from apps.content.models import Content
from apps.report.models import Report
from apps.enums.models import ContentStatus

# List all content for admin
def admin_content_list(request):
    contents = Content.objects.all()  # or filter by status if needed
    return render(request, 'admin/admin_content_list.html', {'contents': contents})


# View content details
def admin_content_detail(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    return render(request, 'admin/content_detail.html', {'content': content})


# Edit content
def admin_content_edit(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    if request.method == 'POST':
        form = ContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            content.is_edited = True
            content.save()
            messages.success(request, 'Content updated successfully.')
            return redirect('admin_content_list')
    else:
        form = ContentForm(instance=content)
    return render(request, 'admin/content_edit.html', {'form': form, 'content': content})


# Soft-delete content
def admin_content_delete(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    content.status = ContentStatus.DELETED
    content.save()
    messages.success(request, 'Content deleted successfully.')
    return redirect('admin_content_list')




# Approve reported content
def admin_content_approve(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    
    # Check if content has any pending reports
    reports = Report.objects.filter(target_type='content', target_user=None, target_content=content, status='pending')
    if not reports.exists():
        messages.error(request, 'This content has no pending reports and cannot be approved via reports panel.')
        return redirect('admin_content_list')
    
    content.status = ContentStatus.ACTIVE
    content.save()
    
    # Optionally resolve related reports
    reports.update(status='resolved')
    
    messages.success(request, 'Reported content approved successfully.')
    return redirect('admin_content_list')


# Reject reported content
def admin_content_reject(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    
    # Check if content has any pending reports
    reports = Report.objects.filter(target_type='content', target_user=None, target_content=content, status='pending')
    if not reports.exists():
        messages.error(request, 'This content has no pending reports and cannot be rejected via reports panel.')
        return redirect('admin_content_list')
    
    content.status = ContentStatus.REJECTED
    content.save()
    
    # Optionally resolve related reports
    reports.update(status='resolved')
    
    messages.success(request, 'Reported content rejected successfully.')
    return redirect('admin_content_list')
