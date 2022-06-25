from django.views.generic.list import ListView
from unicodedata import category
from django.core import paginator
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from user.models import BANK, BankDetails, Education, Profile,  Submitted, Scholarship
from .forms import AddEducationForm, AprovedScholarshipForm, PaymentForm, CreateUserForm, PaymentForm, UserUpdateForm, ProfileUpdateForm, ApplicantBankForm,ConfirmForm,ApplicantsSearchForm, ScholarshipForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, FormView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.views.generic import TemplateView
import json
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import requests
import random

import math


import dotenv

from djangoflutterwave.models import FlwPlanModel
# Create your views here.
def login(request):
    return render(request, 'user/login.html')

class OwnerQuerysetMixin(object):                         
    def get_queryset(self):
        queryset = super(OwnerQuerysetMixin, self).get_queryset()                                                   
        # perhaps handle the case where user is not authenticated
        queryset = queryset.filter(owner=self.request.user)
        return queryset


#Register New User Method
def register(request):
    #Create variable and query all users
    workers = User.objects.all()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registered Successfully.')
            return redirect('user-login')
    else:
        form = CreateUserForm()
    context = {
        'form':form,
        'workers':workers,
    }
    return render(request, 'user/register.html', context)

def logout(request):
    return render(request, 'user/logout.html')


#View Profile Method
@login_required(login_url='user-login')
def profile(request):
    #count submited Applications
    count_submited = Submitted.objects.count()
    user_app = Submitted.objects.filter(applicant =request.user).count()
    
    context = {   
        'count_submited':count_submited,
        'user_app':user_app,
    }
    return render(request, 'user/profile.html', context)
   
#Update Profile Method
@login_required(login_url='user-login')
def profile_update(request):
    if request.method == 'POST':
        #create user form variable
        user_form = UserUpdateForm(request.POST, instance=request.user)
        #create update form variable
        

        profile_form = ProfileUpdateForm(request.POST, request.FILES, 
        instance=request.user.profile)
    #Check if both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully.')
            return redirect('user-education')
            #profile_form.cleaned_data['profilestatus'] ='Updated'
            
            # image = profile_form.cleaned_data['image']

            # if not image:
            #     messages.error(request, 'Passport is Needed.')
            #     return redirect('user-profile-update')

            # else:
                
        else:
            messages.error(request, 'Check Your Passport Image.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_update.html', context)

#Function for Adding Education
@login_required(login_url='user-login')
def add_education(request):
    try:
       check_education = Education.objects.get(applicant=request.user)
       
    except Education.DoesNotExist:
         #Check if the form method is POST
        if request.method == 'POST':
            #Grab the Add Education Form with information and files
            form = AddEducationForm(request.POST, request.FILES)
            #Check if the form is valid
            if form.is_valid():
                #Attach the logged in applicant to the Education Form (User instance)
                form.instance.applicant = request.user
                #Save the form
                form.save()
                #Send Success Message
                messages.success(request, 'Education Added, Add Bank Now To Continue.')
                return redirect('user-bank')
        else:
            form = AddEducationForm()
        context = {
            'form':form,
        }
        return render(request, 'user/add_education.html', context)
    else:
        if check_education.qualification != None:
            return redirect('user-bank')
        else:
            return redirect('app-submit')


#Method for Editing Education
class UpdateEducation(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'user/edit_education.html'
    form_class = AddEducationForm
    model = Education 

    #Function for Checking whether logged in applicant owns the Record
    
    #Function to get Object Product Key for url
    def get_success_url(self):
        return reverse_lazy('education-detail', kwargs = {'pk':self.get_object().id})

    def test_func(self):
        return self.get_object().applicant_id == self.request.user.pk 

        

#Method for viewing Education Detail
class EducationDetail(LoginRequiredMixin, DetailView):
    template_name = 'user/education_detail.html'
    model = Education

    def get_success_url(self):
        return reverse_lazy('app-submit', kwargs = {'pk' : self.get_object().id})
            




#Function for Adding Bank Details for Applicant
@login_required(login_url='user-login')
def AddBankDetails(request):
    try:
        check_bank = BankDetails.objects.get(applicant=request.user)
    except BankDetails.DoesNotExist:
        #Check if the Form method is POST
        if request.method == 'POST':
                    #Create a form and attach the Bank Form to it
                    form = ApplicantBankForm(request.POST, request.FILES)
                    #Check if the Form was a valid one
                    if form.is_valid():
                        #Create an instance of the form as the logged in user
                        form.instance.applicant = request.user
                        #save the form
                        form.save()
                        #send Success message
                        messages.success(request, 'Bank Added; Confirm Application and Print Slip.')
                        #Redirect applicant to The Confirmation Page
                        return redirect('app-submit')
        else:
            form = ApplicantBankForm()

        context = {
                    'form':form,   
                }
        return render(request, 'user/Add_Bank.html', context)
    else:
        if check_bank.account != None:
            return redirect('app-submit')
        else:
            return redirect('app-slip')

class UpdateBank(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    template_name = 'user/edit_bank.html'
    form_class = ApplicantBankForm
    model = BankDetails
    

    def get_success_url(self):
        return reverse_lazy('bank-detail',kwargs={'pk': self.get_object().id})

    def test_func(self):
        return self.get_object().applicant_id == self.request.user.pk 


    

#Bank Detail View
class BankDetailView(LoginRequiredMixin, DetailView):
    template_name = 'user/bank_detail.html'
    model = BankDetails

    def get_success_url(self):
        return reverse_lazy('app-submit', kwargs = {'pk' : self.get_object().id})


#Edit Bank Details


    

        
     
#Method for Application Confirmation and Submission
@login_required(login_url='user-login')
def SubmitApp(request):
    try:
        #Grab the logged in applicant in the submited app table
        check_submited = Submitted.objects.get(applicant=request.user)
    #If it Does NOT Exist then submit it
    except Submitted.DoesNotExist:
        if request.method == 'POST':
            submit_form = ConfirmForm(request.POST, request.FILES)
            if submit_form.is_valid():
                submit_form.instance.applicant = request.user
                submit_form.save()
                messages.success(request, '2022 WASU Scholarship Application Submited Successfully.')
                return redirect('app-slip')
        else:
            submit_form = ConfirmForm()
    
        context = {
            'submit_form':submit_form,
            
        }
        return render(request, 'user/confirmation.html', context)

    else:
        if check_submited.application != "":
            return redirect('app-slip')
        

#Function for Application Confirmation
@login_required(login_url='user-login')
def AppSlip(request):
    #Get Applicant Education Level
    get_education = Education.objects.get(applicant = request.user)
    
    candidate_edu = get_education.qualification

    context = {
        'candidate_edu':candidate_edu, 
    }
    return render(request, 'user/slip.html', context)



#Submited Applications
@login_required(login_url='user-login')
def SubmitedApps(request):
    #Check List of Applicants
    check_submited = Submitted.objects.all()
    #Count Applicants
    count_submited = check_submited.count()

    context = {
        'check_submited':check_submited,
        'count_submited':count_submited,
    }
    return render(request, 'user/list_applicants.html', context)

#Function for Printing Application
@login_required(login_url='user-login')
def print_slip(request):
    
    return render(request, 'user/print_slip.html')

#Success Payment Page
@login_required(login_url='user-login')
def success_payment(request):
    #Get Applicant Education Level
    get_education = Education.objects.get(applicant = request.user)
    
    candidate_edu = get_education.qualification

    context = {
        'candidate_edu': candidate_edu,
    }

    return render(request, 'user/success_payment.html', context)

#Failed Payment Page
@login_required(login_url='user-login')
def failed_payment(request):
    #Get Applicant Education Level
    get_education = Education.objects.get(applicant = request.user)
    
    candidate_edu = get_education.qualification

    context = {
        'candidate_edu': candidate_edu,
    }

    return render(request, 'user/failed_payment.html', context)


#Search Applicants by Nation
@login_required(login_url='user-login')
def search_applicants(request):
    
    form = ApplicantsSearchForm(request.GET or None)
    if form.is_valid():
        list_submited = Profile.objects.filter(
            nation__icontains=form.cleaned_data['nation'],
            state__icontains=form.cleaned_data['state']
        )
    else:
        list_submited = Submitted.objects.all()

    paginator = Paginator(list_submited, 5)
    page = request.GET.get('page')
    paged_listApps = paginator.get_page(page)
   
    context = {
    'list_applicants':paged_listApps,
    'form':form,
   
    
    }

    return render(request, 'user/list_applicants.html',context)


#Method for viewing applicant profile
class ApplicantView(LoginRequiredMixin, DetailView):
    template_name = 'user/view_applicant'
    model = Submitted

#Add Scholarship Function
@login_required(login_url='user-login')
def add_scholarship(request):

    form = ScholarshipForm(request.POST, request.FILES)

    if request.method == 'POST':
        form = ScholarshipForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            messages.success(request, 'Scholarship Added Successfully')
            return redirect('scholarship-list')
    else:
        form = ScholarshipForm()

    context = {
        'form':form
    }
    return render(request, 'user/add_scholarship.html', context)


#List Scholarship
@login_required(login_url='user-login')
def Scholarship_List(request):

    queryset = Scholarship.objects.all()

    context = {
        'scholarship':queryset,
    }
    return render(request, 'user/scholarship_list.html', context)


#Function for getting Candidate Selected Scholarship
@login_required(login_url='user-login')
def scholarship_detail(request, pk):
    data = Scholarship.objects.get(id=pk)

    if request.method=='POST':
        form = PaymentForm(request.POST or None)
        if form.is_valid():
            
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            amount = form.cleaned_data['amount']
            phone = form.cleaned_data['phone']
            context = {'applicant':name, 'email':email, 'amount':amount, 'phone':phone} 
            return process_payment(request, context)    
    else:
        form = PaymentForm()
        

    ctx={
        'form':form,
        'product':data,
        
        
    }
    return render(request, 'user/scholarship_detail.html', ctx)


#Class for Applicant Fee Payment
class PayFeeView(TemplateView):
    template_name = "user/payment_template.html"

    def get_context_data(self, **kwargs):
        """Add payment type to context data"""
        kwargs = super().get_context_data(**kwargs)
        kwargs["pro_plan"] = FlwPlanModel.objects.filter(
            name="Pro Plan"
        ).first()
        return kwargs


from django.http import JsonResponse
#Function for processing Payment
@login_required(login_url='user-login')
def process_payment(request, newContext={}):
    print(newContext)
    auth_token= 'FLWPUBK-fe87eccf0fe3aa4bfcee68205fe4115b-X'
    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
                "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
                "amount":newContext['amount'],
                "currency":"USD",
                "redirect_url":"http://localhost:8000/callback",
                "payment_options":"card",
                "meta":{
                    "consumer_id":23,
                    "consumer_mac":"92a3-912ba-1192a"
                },
                "customer":{
                    "email":newContext['email'],
                    "phonenumber":newContext['phone'],
                    "name":newContext['applicant']
                },
                "customizations":{
                    "title":"WASU Scholarship 2022",
                    "description":"West African Students' Union",
                    "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
                }
                }
    url = ' https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response=response.json()
    print(response)
    link=response['data']
    return JsonResponse(link, safe=False)
    


@require_http_methods(['GET', 'POST'])
def payment_response(request):
    status=request.GET.get('status', None)
    tx_ref=request.GET.get('tx_ref', None)
    print(status)
    print(tx_ref)
    return HttpResponse('Finished')