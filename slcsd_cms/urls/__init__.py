from django.urls import include, path

app_name = 'slcsd_cms'

urlpatterns = [
    path('api/', include('slcsd_cms.urls.api')),
    path('manage/', include('slcsd_cms.urls.admin')),
]
