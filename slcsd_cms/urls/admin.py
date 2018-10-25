from django.urls import reverse_lazy, path
from django.views.generic.base import (
    RedirectView,
    TemplateView,
)
import slcsd_cms.views.admin as admin_views

app_name = 'admin'

urlpatterns = [
    path(
        '',
        admin_views.Home.as_view(),
        name='home',
    ),
    path(
        'dashboard/',
        admin_views.Dashboard.as_view(),
        name='dashboard',
    ),
    path(
        'users/employees/',
        admin_views.Employees.as_view(),
        name='users-employees',
    ),
    path(
        'users/non-employees/',
        admin_views.NonEmployees.as_view(),
        name='users-non-employees',
    ),
    path(
        'users/services/',
        admin_views.Services.as_view(),
        name='users-services',
    ),
    path(
        'users/guests/',
        admin_views.Guests.as_view(),
        name='users-guests',
    ),
    path(
        'groups/',
        admin_views.Groups.as_view(),
        name='groups',
    ),
    path(
        'sites/',
        admin_views.Sites.as_view(),
        name='sites',
    ),
]
