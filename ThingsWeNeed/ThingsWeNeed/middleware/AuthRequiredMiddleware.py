from django.shortcuts import redirect

class AuthRequiredMiddleware():
    def process_request(self, request):
        if not request.user.is_authenticated():
            return redirect('login')
