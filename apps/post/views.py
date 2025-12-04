from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post
from apps.enums.models import ContentStatus

# List all posts
def admin_post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'admin/post_list.html', {'posts': posts})


# View post details
def admin_post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'admin/post_detail.html', {'post': post})


# Soft-delete a post
def admin_post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.status = ContentStatus.DELETED
    post.save()
    messages.success(request, 'Post deleted successfully.')
    return redirect('admin_post_list')
