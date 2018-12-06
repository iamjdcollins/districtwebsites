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
        'login/',
        admin_views.Login.as_view(),
        name='login',
    ),
    path(
        'logout/',
        admin_views.Logout.as_view(),
        name='logout',
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
    path(
        'sites/<uuid:site>/',
        admin_views.Site.as_view(),
        name='site',
    ),
    path(
        'sites/<uuid:site>/dashboard/',
        admin_views.SiteDashboard.as_view(),
        name='site-dashboard',
    ),
    path(
        'sites/<uuid:site>/domains/',
        admin_views.SiteDomains.as_view(),
        name='site-domains',
    )
]
