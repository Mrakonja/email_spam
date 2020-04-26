from django.views.generic import TemplateView, ListView, View, FormView, DeleteView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import User_Agents, Addresses, Proxies, SendingDomains, SpamDomains, UsageLog,MailsBatch
from .forms import SendingDomainsForm, SpamDomainsForm
from .tasks import sec_remove, mail_cheker
from datetime import datetime

class UsageLog(ListView):
   template_name = 'email_sender/UsageLog.html'
   model = UsageLog

class Batches(ListView):
   template_name = 'email_sender/Batches.html'
   model = MailsBatch

def imtp(request, id):
   query = Addresses.objects.filter(MailsBatch_id=id)
   mail_cheker(query)
   return redirect('mailstable')



def removesecurity(request, id):
   adrs = Addresses.objects.get(pk=id)
   sec_remove(adrs.Email ,adrs.Password, adrs.Secret)
   return redirect('mailstable')

class Emails(TemplateView):
    template_name = "email_sender/home.html"


class SpamDomainsView(ListView):
   template_name = 'email_sender/spamtable.html'
   model = SpamDomains
   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = SpamDomainsForm
      return context

   def post(self, request, *args, **kwargs):
      form =SpamDomainsForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('spamtable')

      return render(request, self.template_name, {'form': form})

class SendingDomainsView(ListView):
   template_name = 'email_sender/sendingtable.html'
   model =  SendingDomains

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = SendingDomainsForm
      return context

   def post(self, request, *args, **kwargs):
      form = SendingDomainsForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('sendingtable')

      return render(request, self.template_name, {'form': form})

class Imports(TemplateView):
   template_name = "email_sender/import.html"
   
class MailsTable(ListView):
      template_name = "email_sender/mailstable.html"
      model = Addresses
      
class ProxiesTable(ListView):
   template_name = "email_sender/proxiestable.html"
   model = Proxies
   
class UseragentsTable(ListView):
   template_name = "email_sender/uatables.html"
   model = User_Agents

def upload_mails(request):
   if "GET" == request.method:
      return render(request, "status")
   
   try:
      csv_file = request.FILES["csv_file"]
      
      if not csv_file.name.endswith('.csv'):
         print('File is not CSV type')
         return HttpResponseRedirect("status")
      
      if csv_file.multiple_chunks():
         print("Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
         return HttpResponseRedirect("status")
      
      file_data = csv_file.read().decode("utf-8")
      lines = file_data.split("\n")
      d =  datetime.now()
      new_batch = MailsBatch(Date=d, Name="batch"+ d.strftime('%Y-%m-%d-%H%M%S'))
      new_batch.save()
      for line in lines:
         try:
            fields = line.split(",")
            result = Addresses(Email = fields[0],
                                Password = fields[1],
                                Secret = fields[2],
                                Active =  'N',
                                MailsBatch = new_batch
                                )
            result.save()


         except Exception as e:
             print(e)

   

   
   except Exception as e:
      print("Unable to upload file. " + repr(e))
      

   
   return HttpResponseRedirect("imports")

class SendingDomainsDelete(DeleteView):
   model= SendingDomains
   success_url = reverse_lazy('sendingtable')

class SpamDomainsDelete(DeleteView):
   model = SpamDomains
   success_url = reverse_lazy('spamtable')

def  UsageLog(request):
   template_name = 'email_sender/UsageLog.html'

