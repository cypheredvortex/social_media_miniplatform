from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from bson import ObjectId
from .models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:50]
    
    return render(request, 'notification/list.html', {
        'notifications': notifications
    })

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(
        Notification, 
        id=ObjectId(notification_id),
        user=request.user
    )
    notification.mark_as_read()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notification:list')

@login_required
def mark_all_read(request):
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    return redirect('notification:list')