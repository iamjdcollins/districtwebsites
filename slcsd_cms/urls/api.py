from rest_framework import routers

from django.urls import path, include

from ..views import api

router = routers.DefaultRouter(trailing_slash=True)
router.APIRootView = api.APIRootView
router.register(r'users', api.UserViewSet, 'user')
router.register(r'sites', api.SiteViewSet, 'site')
router.register(r'domains', api.DomainViewSet, 'domain')
router.register(r'groups', api.GroupViewSet, 'group')

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
]
