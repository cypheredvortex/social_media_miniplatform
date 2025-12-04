from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Comment
from apps.enums.models import ContentStatus

# List all comments
def admin_comment_list(request):
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'admin/admin_comment_list.html', {'comments': comments})


# View comment details
def admin_comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return render(request, 'admin/comment_detail.html', {'comment': comment})


# Soft-delete a comment
def admin_comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.status = ContentStatus.DELETED
    comment.save()
    messages.success(request, 'Comment deleted successfully.')
    return redirect('comment:admin_comment_list')
