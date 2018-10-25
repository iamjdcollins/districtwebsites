from django.urls import reverse_lazy
from django.views.generic.base import (
    RedirectView,
    TemplateView,
)


class Home(RedirectView):
    url = reverse_lazy('slcsd_cms:admin:dashboard')

    class Meta:
        breadcrumb_title = 'Home'
        breadcrumb_icon = 'icon-home2'


class Dashboard(TemplateView):
    template_name = 'slcsd_cms/base.html'

    class Meta:
        breadcrumb_title = 'Dashboard'
        breadcrumb_icon = None


class Employees(TemplateView):
    template_name = 'slcsd_cms/users-employees.html'

    class Meta:
        breadcrumb_title = 'Employees'
        breadcrumb_icon = None


class NonEmployees(TemplateView):
    template_name = 'slcsd_cms/users-non-employees.html'

    class Meta:
        breadcrumb_title = 'Non-Employees'
        breadcrumb_icon = None


class Services(TemplateView):
    template_name = 'slcsd_cms/users-services.html'

    class Meta:
        breadcrumb_title = 'Service Accounts'
        breadcrumb_icon = None


class Guests(TemplateView):
    template_name = 'slcsd_cms/users-guests.html'

    class Meta:
        breadcrumb_title = 'Guests'
        breadcrumb_icon = None


class Groups(TemplateView):
    template_name = 'slcsd_cms/groups.html'

    class Meta:
        breadcrumb_title = 'Groups'
        breadcrumb_icon = None


class Sites(TemplateView):
    template_name = 'slcsd_cms/sites.html'

    class Meta:
        breadcrumb_title = 'Sites'
        breadcrumb_icon = None
