from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import User_Agents, Addresses, Proxies


class Emails(TemplateView):
    template_name = "email_sender/home.html"
class Imports(FormView):
   template_name = "email_sender/import.html"
class Proxies(TemplateView):
   template_name = "email_sender/home.html"

class SendingDomains(TemplateView):
      template_name = "email_sender/home.html"
   
class SpamDomains(TemplateView):
      template_name = "home.html"
   
class UsageLog(TemplateView):
      template_name = "home.html"
 

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
      
      for line in lines:
         try:
            fields = line.split(",")
            data = functions.getSheetData(fields)
            try:
               resultDB = Addresses(
                                 )
               resultDB.save()
            except:
               pass
         except:
            pass
   

   
   except Exception as e:
      print("Unable to upload file. " + repr(e))
      

   
   return HttpResponseRedirect("status")


def upload_proxies(request):
   if "GET" == request.method:
      return render(request, "status")
   
   try:
      csv_file = request.FILES["csv_file"]
      email = price = address = 0
      if 'email' in request.GET:
         email = 1
      if 'price' in request.GET:
         price = 1
      if 'address' in request.GET:
         address = 1
      
      if not csv_file.name.endswith('.csv'):
         print('File is not CSV type')
         return HttpResponseRedirect("status")
      
      if csv_file.multiple_chunks():
         print("Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
         return HttpResponseRedirect("status")
      
      file_data = csv_file.read().decode("utf-8")
      lines = file_data.split("\n")
      
      for line in lines:
         try:
            fields = line.split(",")
            data = functions.getSheetData(fields)
            try:
               resultDB = Result(uid='UPLOAD',
                                 name=data['name'],
                                 yurl=data['yurl'],
                                 review_count='',
                                 address=data['address'],
                                 city=data['city'],
                                 state=data['state'],
                                 categories='',
                                 phone=data['phone'],
                                 surl=data['surl'],
                                 rating=''
                                 )
               resultDB.save()
            except:
               pass
         except:
            pass
      
      searchDB = Search(
         term='various',
         location='various',
         date='various',
         uid='UPLOAD',
      )
      searchDB.save()
   
   
   except Exception as e:
      print("Unable to upload file. " + repr(e))
   
   return HttpResponseRedirect("status")


def upload_useragents(request):
   if "GET" == request.method:
      return render(request, "status")
   
   try:
      csv_file = request.FILES["csv_file"]
      email = price = address = 0
      if 'email' in request.GET:
         email = 1
      if 'price' in request.GET:
         price = 1
      if 'address' in request.GET:
         address = 1
      
      if not csv_file.name.endswith('.csv'):
         print('File is not CSV type')
         return HttpResponseRedirect("status")
      
      if csv_file.multiple_chunks():
         print("Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
         return HttpResponseRedirect("status")
      
      file_data = csv_file.read().decode("utf-8")
      lines = file_data.split("\n")
      
      for line in lines:
         try:
            fields = line.split(",")
            data = functions.getSheetData(fields)
            try:
               resultDB = Result(uid='UPLOAD',
                                 name=data['name'],
                                 yurl=data['yurl'],
                                 review_count='',
                                 address=data['address'],
                                 city=data['city'],
                                 state=data['state'],
                                 categories='',
                                 phone=data['phone'],
                                 surl=data['surl'],
                                 rating=''
                                 )
               resultDB.save()
            except:
               pass
         except:
            pass
      
      searchDB = Search(
         term='various',
         location='various',
         date='various',
         uid='UPLOAD',
      )
      searchDB.save()
   
   
   except Exception as e:
      print("Unable to upload file. " + repr(e))
   
   return HttpResponseRedirect("status")
