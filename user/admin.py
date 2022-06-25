from django.contrib import admin
from . models import Profile, Education, BankDetails,Submitted, Scholarship, Payment
# Register your models here.
admin.site.register(Profile)

admin.site.register(Education)

admin.site.register(BankDetails)

admin.site.register(Submitted)

admin.site.register(Scholarship)

admin.site.register(Payment) 
