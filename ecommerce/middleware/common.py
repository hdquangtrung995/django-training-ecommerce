from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404

from ecommerce.models import EcomCategory, EcomStore, EcomStoreGuideline


class CommonDataMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        categories = EcomCategory.objects.select_related("parent").all()
        store = get_object_or_404(EcomStore, pk=1)
        guidelineSerialized = get_list_or_404(EcomStoreGuideline)

        request.common_data = {
            "categories": categories,
            "store_context": store,
            "guideline_context": guidelineSerialized,
        }
        return None

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response):
        # process_template_response() is called just after the view has finished executing, if the response instance has a render() method, indicating that it is a TemplateResponse or equivalent.
        # It must return a response object that implements a render method
        return response
