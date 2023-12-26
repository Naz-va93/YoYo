from .forms import CaptchaForm

class CaptchaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.captcha_form = CaptchaForm()
        response = self.get_response(request)
        return response