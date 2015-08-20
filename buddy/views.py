from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

class BaseView(TemplateView):
    template_name = 'base.html'
    
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)