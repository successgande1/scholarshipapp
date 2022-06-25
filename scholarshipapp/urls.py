"""scholarshipapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
#Import user app and its views module
from user import views as user_view
from django.contrib.auth import views as auth_view
from user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('register/', user_view.register, name = 'user-register'),
    path('profile/', user_view.profile, name = 'user-profile'),
    path('profile/update/', user_view.profile_update, name = 'user-profile-update'),
    path('', auth_view.LoginView.as_view(template_name='user/login.html'), name = 'user-login'),
    path('education/', user_view.add_education, name = 'user-education'),
    path('<int:pk>/education/update/', UpdateEducation.as_view(), name = 'edit-education'),
    path('<int:pk>/education/detail/', EducationDetail.as_view(), name = 'education-detail'),
    path('bank/', user_view.AddBankDetails, name = 'user-bank'),
    path('scholarship/', user_view.add_scholarship, name = 'add-scholarship'),
    path('scholarship/list/', user_view.Scholarship_List, name = 'scholarship-list'),
    path('<int:pk>/bank/update/', UpdateBank.as_view(), name = 'edit-bank'),
    path('<int:pk>/bank/detail/', BankDetailView.as_view(), name = 'bank-detail'),
    path('applicants/search/', user_view.search_applicants, name = 'search-applicants'),
    path('applicant/submit/', user_view.SubmitApp, name = 'app-submit'),
    path('applicant/slip/', user_view.AppSlip, name = 'app-slip'),
    path('applicant/slip/print/', user_view.print_slip, name = 'print-slip'),
    
    path('applicants/', user_view.SubmitedApps, name = 'list-applicants'),
    path('applicant/payment/success/', user_view.success_payment, name = 'success-payment'),
    path('applicant/payment/failed/', user_view.failed_payment, name = 'failed-payment'),
    path('candidate/<int:pk>/scholarship/', user_view.scholarship_detail, name = 'candidate-scholarship'),
    path('callback', user_view.payment_response, name='payment_response'),
    path('sholarship/process/', user_view.process_payment, name = 'process-fee'),
    path('pay/', PayFeeView.as_view(), name ="pay"),
    
    path('logout/', auth_view.LogoutView.as_view(template_name='user/logout.html'), name = 'user-logout'),
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='user/password_reset.html'), name = 'password_reset'),
    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name ='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('reset_password_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name = 'password_reset_complete'),
]+ static ( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


handler404 = "scholarshipapp.views.page_not_found_view"