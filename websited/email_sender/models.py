from django.db import models


ACTIVE_CHOICES = [
    ('A', 'ACTIVE'),
    ('N', 'NOTACTIVe'),
]
#
# class Email(models.Model):
#       ProxyIP = models.CharField(max_length=255)
#

class Addresses(models.Model):
      Email = models.EmailField()
      Password = models.CharField(max_length=255)
      Secret = models.CharField(max_length=255)
      Active =  models.CharField(max_length=1, choices=ACTIVE_CHOICES)
#
 class Proxies(models.Model):
       Domain = models.CharField(max_length=255)
       Active =  models.CharField(max_length=1, choices=ACTIVE_CHOICES)

# class SendingDomains(models.Model):
#       Domain = models.CharField(max_length=255)
#       Active =  models.CharField(max_length=1, choices=ACTIVE_CHOICES)
#
# class SpamDomains(models.Model):
#       Domain = models.CharField(max_length=255)
#       Active =  models.CharField(max_length=1, choices=ACTIVE_CHOICES)
#
# class Responses(models.Model):
#       Response = models.CharField(max_length=255)
#       Active =  models.CharField(max_length=1, choices=ACTIVE_CHOICES)
#
class User_Agents(models.Model):
      User_Agent = models.CharField(max_length=255)
      Software = models.CharField(max_length=255)
      OS = models.CharField(max_length=255)
      Layout_Engine = models.CharField(max_length=255)
      Weight = models.CharField(max_length=255)
#
# class UsageLog(models.Model):
#       Proxies_ID =
#       EmailAddresses_ID =
#       Number_Opened =
#       Number_Clicked =
#       Number_Retreived_from_Spam =
#       Number_Spam =
#       timestamp =