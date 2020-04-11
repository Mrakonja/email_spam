from django.contrib import admin
from django.urls import path, include
from .views import Emails, Imports, upload_mails, upload_useragents, upload_proxies

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Emails.as_view(), name='index'),
    path('imports',Imports.as_view(), name='imports'),
    path('uploadmails',upload_mails, name='uploadmails'),
    path('uploadproxies', upload_proxies, name='uploadproxies'),
    path('uploaduseragents', upload_useragents, name='uploaduseragents'),
]
