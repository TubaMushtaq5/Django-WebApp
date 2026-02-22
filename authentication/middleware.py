from django.shortcuts import redirect
from django.urls import resolve

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.public_view_names = ['login', 'signup']

    def __call__(self, request):

        if request.path.startswith('/admin/'):
            return self.get_response(request)

        current_view = resolve(request.path_info).url_name

        if not request.user.is_authenticated and current_view not in self.public_view_names:
            return redirect('login')

        return self.get_response(request)