from django.shortcuts import HttpResponse,render
from django.middleware.common import MiddlewareMixin

class AdminOnlyMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path == ['/add_products/' ,'/add_categories/','/update_products/'] :
            if not request.user.is_staff:
                unauthorized_content = render(request, 'store/unavalable_page.html').content
                return HttpResponse(unauthorized_content, status=403)
        return response