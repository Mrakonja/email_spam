from django.contrib import admin
from django.urls import path, include
from .views import (Emails, Imports,upload_mails, MailsTable,
                    imtp, removesecurity, SendingDomainsView,
                    SpamDomainsView, SendingDomainsDelete,SpamDomainsDelete, UsageLog, Batches)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', Emails.as_view(), name='index'),
    path('imports/', Imports.as_view(), name='imports'),
    
    path('uploadmails', upload_mails, name='uploadmails'),

    path('imtp/<int:id>/', imtp, name='imtp'),
    # path('webdriver/<int:id>/', webdriver, name='webdriver'),
    path('removesecurity/<int:id>/', removesecurity, name='removesecurity'),

    path('mailstable/', MailsTable.as_view(), name='mailstable'),
    path('usagelog/', UsageLog, name='usagelog'),
    path('batches/', Batches.as_view(), name='batches'),
    path('batches/<int:id>/', imtp, name='batchesscan'),

    path('sendingtable/', SendingDomainsView.as_view(), name='sendingtable'),
    path('spamtable/', SpamDomainsView.as_view(), name='spamtable'),
    path('deletesendingdomain/<int:pk>', SendingDomainsDelete.as_view(), name='deletesendingdomain'),
    path('deletespamdomain/<int:pk>', SpamDomainsDelete.as_view(), name='deletespamdomain'),
]
