from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
import datetime
from django.contrib.auth.models import User
from django.contrib import messages

from user.models import Profile, Submitted

# Create your views here.
@login_required(login_url='user-login')
def index(request):
    
    #Grab the logged in user
    user = request.user 
    #Check if user was authenticated 
    if user.is_authenticated:
        try:
            #Try to get the profile of the logged in user
            profile = Profile.objects.get(applicant=user) 
        except Profile.DoesNotExist:
            #Unless it does not exist then throw Error and redirect
            messages.error(request, 'Profile DOES NOT EXIST!')
            # Redirect to a Profile creating page?
            return redirect('user-register')
        else:
            #count submited Applications
            count_submited = Submitted.objects.count()
            user_app = Submitted.objects.filter(applicant =request.user).count()
            context = {
                'count_submited':count_submited,
                'user_app':user_app,

            }
        return render(request, 'user/profile.html', context)
            
            # #Check if the logged in user profile surname field is not yet Updated
            # if profile.surname == None or profile.image == 'avatar.jpg':
            #     #Redirect user to update his/her profile information
            #     return redirect('user-profile-update')
            # else:
                #Redirect user to view his profile information
                
    
    
    

  