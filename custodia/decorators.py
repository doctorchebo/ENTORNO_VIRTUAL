from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args,**kwargs):
        if request.user.is_authenticated:
            return redirect('login')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args,**kwargs):
            group = None
            if request.user.groups.filter(name__in=allowed_roles).exists():
                # group = request.user.groups.all()[0].name
                return  view_func(request, *args,**kwargs)
            # if group in allowed_roles:
            else:
                return HttpResponse('No está autorizado para ejecutar esta acción')
        return wrapper_func
    return decorator    