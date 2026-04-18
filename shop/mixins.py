from django.contrib import messages
from django.shortcuts import redirect


def role_required(*allowed_roles):
    def decorator(view_func):
        def wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            role = getattr(getattr(request.user, 'profile', None), 'role', None)
            if role not in allowed_roles:
                messages.error(request, 'У вас нет прав для выполнения этого действия.')
                return redirect('catalog')
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
