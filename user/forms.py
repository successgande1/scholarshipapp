from crispy_forms.helper import FormHelper
from django import forms
from .models import Profile, Submitted
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Education, BankDetails, Submitted, Scholarship, Payment
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget




class AddEducationForm(forms.ModelForm):
    
    instition = forms.CharField(label="Institution Name (Nom de l'institution):", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Full Name and and Address of Institution'}))
    matnumber = forms.CharField(label="Admission Number (Numéro d'immatriculation) :", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Admission/Matriculation Number'}))
    reference = forms.CharField(label='Applicant\'s Referee (Arbitre du candidat):', 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Referee Full Name'}))
    refphone = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial="NG")
    )
    reasons = forms.CharField(label="Reason for Scholarship (Raison de la bourse):", 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Reason for the Scholarship. (Raison de la bourse)'}))
    
    class Meta:
        model = Education
        fields = ['qualification','instition', 'matnumber', 'reference', 'refphone', 'reasons']


class CreateUserForm(UserCreationForm):
    email = forms.EmailField

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#Update user Form
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']

#Update Profile Form
class ProfileUpdateForm(forms.ModelForm):
    surname = forms.CharField(label='Surname:', widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Inherited Family Name.'}))
    othernames = forms.CharField(label='Other Names:', widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s First and Middle Name(s).'}))
    phone = PhoneNumberField(
        widget = PhoneNumberPrefixWidget(initial="NG")
    )
    state = forms.CharField(label='State/Province:', widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s State/Province of Origin.'}))
    image = forms.ImageField(required=True)
    class Meta:
        model = Profile
        fields = ['surname', 'othernames', 'phone', 'nation', 'state', 'image']
        
        
    
    #  def clean_image(self):
    #     image = self.cleaned_data.get('image')
    #     if not image or image == "":
    #         raise forms.ValidationError(('Invalid value'), code='invalid') 
    #     return image 

#Add Bank Details Form
class ApplicantBankForm(forms.ModelForm):
    bank = forms.CharField(label='Bank Name:', 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Account Name'}))
    
    account = forms.CharField(label='Account Number:', 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Account Number'}))
    name = forms.CharField(label='Account Name:', 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Account Name'}))
    branch = forms.CharField(label='Bank Branch', 
                    widget=forms.TextInput(attrs={'placeholder': 'Applicant\'s Bank Branch'}))
    class Meta:
        model = BankDetails
        fields = ['bank', 'account', 'name', 'branch']

class ConfirmForm(forms.ModelForm):
    confirm = forms.BooleanField()
    class Meta:
        model = Submitted
        fields = ['confirm'] 

class ApplicantsSearchForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['nation', 'state']

class AprovedScholarshipForm(forms.ModelForm):
    confirm = forms.BooleanField()
    
    class Meta:
        model = Submitted
        fields = ['approved']
        

class ScholarshipForm(forms.ModelForm):

    class Meta:
        model = Scholarship
        fields = ['name', 'category', 'amount',  'fee']

#candidate scholarship form
class PaymentForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField()
    phone=forms.CharField(max_length=15)
    amount = forms.FloatField()


#Search Applicant form
class SearchApplicantForm(forms.Form):
    value = forms.CharField(label = 'Applicant Name', max_length=30)
