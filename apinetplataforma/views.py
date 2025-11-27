from django.views.generic import TemplateView


class BaseView(TemplateView):
    template_name = "base.html"


class DashboardView(TemplateView):
    template_name = "dashboard.html"