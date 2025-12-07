def user_context(request):
    return {
        'current_user': request.user if hasattr(request, 'user') else None
    }