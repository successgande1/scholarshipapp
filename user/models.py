from unicodedata import category
import uuid
from urllib.parse import MAX_CACHE_SIZE
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import RegexValidator
from django.forms import CharField
from phonenumber_field.modelfields import PhoneNumberField

GENDER = (
	('Male', 'Male'),
	('Female', 'Female'),
)

NATION = (
	('Benin Republic', 'Benin Republic'),
	('Burkina Faso', 'Burkina Faso'),
    ('Cape Verde', 'Cape Verde'),
    ('Cote D\'Ivoire', 'Cote D\'Ivoire'),
    ('Gambia', 'Gambia'),
    ('Ghana', 'Ghana'),
    ('Guinea', 'Guinea'),
    ('Guinea-Bissau', 'Guinea-Bissau'),
    ('Liberia', 'Liberia'),
    ('Mali', 'Mali'),
    ('Mauritania', 'Mauritania'),
    ('Niger', 'Niger'),
    ('Nigeria', 'Nigeria'),
    ('Senegal', 'Senegal'),
    ('Sierra Leone', 'Sierra Leone'),
    ('Togo', 'Togo'),
)

INSTITUTE = (
    ('Secondary School', 'Secondary School'),
    ('Undergraduate', 'Undergraduate'),
    ('Post Graduate', 'Post Graduate'),
)

BANK = (
    ('UBA Bank', 'UBA Bank'),
    ('ZENITH BANK', 'ZENITH BANK'),
    ('First Bank of Nigeria', 'First Bank of Nigeria'),
    ('FBNBank Gambia Ltd', 'FBNBank Gambia Ltd'),
    ('Ecobank', 'Ecobank'),
    ('Access Bank', 'Access Bank'),
    ('GTBank', 'GTBank'),
    
)


class Profile(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    surname = models.CharField(max_length=20, null=True)
    othernames = models.CharField(max_length=40, null=True)
    gender = models.CharField(max_length=6, choices=GENDER, blank=True, null=True)
    nation = models.CharField(max_length=255, choices=NATION, blank=True, null=True)
    state = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = PhoneNumberField()
    image = models.ImageField(default='avatar.jpg', blank=False, null=False, upload_to ='profile_images', 
   
    )
    

    #Method to save Image
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
    #Check for Image Height and Width then resize it then save
        if img.height > 200 or img.width > 150:
            output_size = (150, 250)
            img.thumbnail(output_size)
            img.save(self.image.path)
            

    

    def __str__(self):
        return f'{self.applicant.username}-Profile'

#Application Table
class Education(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    qualification = models.CharField(max_length=60, choices=INSTITUTE, default=None, null=True)
    instition = models.CharField(max_length=200, null=True)
    reasons = models.CharField(max_length=100, null=True) 
    matnumber = models.CharField(max_length=255, null=True)
    reference = models.CharField(max_length=100, null=True)
    refphone = PhoneNumberField()
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.applicant}-Education'

class BankDetails(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    account = models.CharField(max_length=20, blank=True, default=None, null = True)
    name = models.CharField(max_length=100, blank=True, null=True)
    branch = models.CharField(max_length=60, blank=True, null = True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.applicant}-Bank'

class Submitted(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    application = models.UUIDField(primary_key = True, editable = False, default=uuid.uuid4)
    confirm = models.BooleanField()
    approved = models.CharField(max_length=20, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
         self.application == str(uuid.uuid4())
         super().save(*args, **kwargs)

    def __unicode__(self):
        return self.applicant 

    def __str__(self):
        return f'Application Number: {self.application}-{self.applicant}'




class Scholarship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    name = models.CharField(max_length=100, null = True)
    fee = models.FloatField()
    category = models.CharField(max_length=60, choices=INSTITUTE, default=None, null=True)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'WASU Scholarship: {self.name}-{self.name}'

class Payment(models.Model):
    applicant = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    email = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=20, null=True)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'WASU Payments: {self.applicant}-{self.amount}'

class Approved(models.Model):
    applicant = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    reference = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'WASU Scholarship Approval {self.applicant}'