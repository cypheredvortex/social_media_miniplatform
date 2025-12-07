from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from bson import ObjectId
from django.db.models import Q

from apps.content.models import Content, Post, Comment
from apps.enums.models import ContentStatus
from apps.user.models import User
from .forms import ContentForm

# ---------------------------
# Admin Content Views
# ---------------------------

def admin_content_list(request):
    # FIXED: Use select_related to optimize queries
    contents = Content.objects.select_related('author').all().order_by('-created_at')
    return render(request, 'admin/admin_content_list.html', {'contents': contents})

def admin_content_detail(request, content_id):
    try:
        # FIXED: Use select_related here too
        content = Content.objects.select_related('author').get(id=ObjectId(content_id))
    except (Content.DoesNotExist, Exception):
        raise Http404("Content not found")
    
    return render(request, 'admin/admin_content_detail.html', {'content': content})

def admin_content_delete(request, content_id):
    try:
        content = get_object_or_404(Content, id=ObjectId(content_id))
    except Exception:
        raise Http404("Content not found")
    
    content.status = ContentStatus.DELETED
    content.save()
    messages.success(request, 'Content deleted successfully.')
    return redirect('content:admin_content_list')

def admin_content_mark_flagged(request, content_id):
    try:
        content = get_object_or_404(Content, id=ObjectId(content_id))
    except Exception:
        raise Http404("Content not found")
    
    content.status = ContentStatus.FLAGGED
    content.save()
    messages.success(request, "Content has been flagged.")
    return redirect('content:admin_content_list')

def debug_content(request):
    from apps.content.models import Content
    from apps.user.models import User
    
    # Check if we have data
    content_count = Content.objects.count()
    user_count = User.objects.count()
    
    # Get first few content items
    contents = Content.objects.all()[:5]
    
    debug_info = []
    for content in contents:
        debug_info.append({
            'id': str(content.id),
            'content_type': content.content_type,
            'author_id': content.author_id,
            'author_exists': content.author is not None,
            'author_username': content.author.username if content.author else None,
            'text': content.text[:50] if content.text else None
        })
    
    return render(request, 'debug.html', {
        'content_count': content_count,
        'user_count': user_count,
        'debug_info': debug_info
    })

# ---------------------------
# Regular User Content Views
# ---------------------------

@login_required
def content_create(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.author = request.user
            content.content_type = 'POST'
            content.media_type = 'TEXT'  # Default, can be overridden
            
            # Handle media upload if present
            if 'media_file' in request.FILES:
                # In production, you'd upload to a service like S3
                content.media_url = f"/media/{request.FILES['media_file'].name}"
                if request.FILES['media_file'].content_type.startswith('image'):
                    content.media_type = 'IMAGE'
                elif request.FILES['media_file'].content_type.startswith('video'):
                    content.media_type = 'VIDEO'
            
            content.save()
            messages.success(request, 'Content created successfully!')
            return redirect('content:detail', content_id=content.id)
    else:
        form = ContentForm()
    
    return render(request, 'content/create.html', {'form': form})

@login_required
def content_detail(request, content_id):
    try:
        content = Content.objects.select_related('author').get(id=ObjectId(content_id))
    except (Content.DoesNotExist, Exception):
        raise Http404("Content not found")
    
    # Check visibility
    if content.visibility == 'PRIVATE' and content.author != request.user:
        messages.error(request, 'This content is private.')
        return redirect('pages:home_page')
    
    replies = content.replies.all().order_by('created_at')
    return render(request, 'content/detail.html', {
        'content': content,
        'replies': replies
    })

@login_required
def content_edit(request, content_id):
    try:
        content = get_object_or_404(Content, id=ObjectId(content_id))
    except Exception:
        raise Http404("Content not found")
    
    # Check permission
    if content.author != request.user:
        messages.error(request, 'You cannot edit this content.')
        return redirect('content:detail', content_id=content_id)
    
    if request.method == 'POST':
        form = ContentForm(request.POST, instance=content)
        if form.is_valid():
            content = form.save(commit=False)
            content.is_edited = True
            content.save()
            messages.success(request, 'Content updated successfully!')
            return redirect('content:detail', content_id=content_id)
    else:
        form = ContentForm(instance=content)
    
    return render(request, 'content/edit.html', {'form': form, 'content': content})

@login_required
def content_delete(request, content_id):
    try:
        content = get_object_or_404(Content, id=ObjectId(content_id))
    except Exception:
        raise Http404("Content not found")
    
    # Check permission
    if content.author != request.user and not request.user.role == 'ADMIN':
        messages.error(request, 'You cannot delete this content.')
        return redirect('content:detail', content_id=content_id)
    
    content.soft_delete()
    messages.success(request, 'Content deleted successfully.')
    return redirect('pages:home_page')

@login_required
@require_POST
def add_comment(request, content_id):
    try:
        parent_content = get_object_or_404(Content, id=ObjectId(content_id))
    except Exception:
        raise Http404("Content not found")
    
    text = request.POST.get('text', '').strip()
    if not text:
        messages.error(request, 'Comment text cannot be empty.')
        return redirect('content:detail', content_id=content_id)
    
    comment = Content.objects.create(
        author=request.user,
        text=text,
        content_type='COMMENT',
        parent_content=parent_content,
        media_type='TEXT'
    )
    
    messages.success(request, 'Comment added successfully!')
    return redirect('content:detail', content_id=content_id)