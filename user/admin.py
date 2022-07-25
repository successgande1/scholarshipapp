from django.contrib import admin
from . models import Profile, Education, BankDetails,Submitted, Scholarship, Payment
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'surname', 'othernames', 'phone', 'state')
    list_per_page = 25

admin.site.register(Profile, ProfileAdmin)

admin.site.register(Education)

admin.site.register(BankDetails)

class SubmittedAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'application', 'confirm', 'approved', 'date')
    list_per_page = 20

admin.site.register(Submitted, SubmittedAdmin)

admin.site.register(Scholarship)

admin.site.register(Payment) 
