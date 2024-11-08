from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime
from django.dispatch import receiver
from django.core.validators import MinLengthValidator
COUNTRIES = (
    ("United Kingdom", "United Kingdom"),
    ("France", "France"),
    ("Germany", "Germany"),
    ("Italy", "Italy"),
    ("Spain", "Spain"),
    ("Greece", "Greece"),
    ("Switzerland", "Switzerland"),
    ("Austria", "Austria"),
    ("Netherlands", "Netherlands"),
    ("Portugal", "Portugal"),
    ("Sweden", "Sweden"),
    ("Denmark", "Denmark"),
    ("Norway", "Norway"),
    ("Finland", "Finland"),
    ("Belgium", "Belgium"),
    ("Ireland", "Ireland"),
    ("Iceland", "Iceland"),
    ("United States", "United States"),
    ("Canada", "Canada"),
    ("Mexico", "Mexico"),
    ("China", "China"),
    ("JP", "Japan"),
    ("India", "India"),
    ("South Korea", "South Korea"),
    ("Indonesia", "Indonesia"),
    ("Thailand", "Thailand"),
    ("Malaysia", "Malaysia"),
    ("Philippines", "Philippines"),
    ("Vietnam", "Vietnam"),
    ("Singapore", "Singapore"),
    ("Taiwan", "Taiwan"),
    ("Hong Kong", "Hong Kong"),
    ("Macau", "Macau"),
    ("Brazil", "Brazil"),
    ("Argentina", "Argentina"),
    ("Colombia", "Colombia"),
    ("Peru", "Peru"),
    ("Chile", "Chile"),
    ("Venezuela", "Venezuela"),
    ("Australia", "Australia"),
    ("New Zealand", "New Zealand"),
    ("South Africa", "South Africa"),
    ("Egypt", "Egypt"),
    ("Morocco", "Morocco"),
    ("Algeria", "Algeria"),
    ("Nigeria", "Nigeria"),
    ("Bahrain", "Bahrain"),
    ("Kuwait", "Kuwait"),
    ("Oman", "Oman"),
    ("Qatar", "Qatar"),
    ("Saudi Arabia", "Saudi Arabia"),
    ("United Arab Emirates", "United Arab Emirates"),
    ("Algeria", "Algeria"),
    ("Libya", "Libya"),
    ("Morocco", "Morocco"),
    ("Sudan", "Sudan"),
    ("Tunisia", "Tunisia"),
)

GENDER_CHOICES = (
    ('Male','Male'),
    ('Female','Female'),
)
# create profile for customers
class Profile(models.Model):
    first_name         = models.CharField(max_length = 50,default = None,verbose_name = 'First Name',null=True,blank=True)
    last_name          = models.CharField(max_length = 50,default = None,null=True,blank=True,verbose_name = 'Last Name')
    email              = models.EmailField(max_length = 50,default = None,unique=True,null=True,blank=True)
    gender             = models.CharField(max_length = 50,choices=GENDER_CHOICES,null=True,blank=True,default ='Male')
    profile_image      = models.ImageField(upload_to ='images/users_profile_images/',null=True,blank=True)
    address            = models.CharField(max_length = 400,default = None, verbose_name = 'Address' ,null=True,blank=True)
    phone              = models.CharField(max_length=11,default = None,null=True,blank=True,validators = [
        MinLengthValidator(11,'The Field Must be contain 11 Numbers')
    ])
    city               = models.CharField(max_length = 200,blank = True)
    state              = models.CharField(max_length = 200,blank = True)
    zipcode            = models.CharField(max_length = 200,blank = True)
    country            =  models.CharField(max_length = 200,blank = True,choices = COUNTRIES)
    joined_at          = models.DateTimeField(default=datetime.now)
    user               = models.OneToOneField(User,on_delete=models.CASCADE)
    cart               = models.CharField(max_length = 200,null= True,blank = True) 
    def __str__(self):
        if self.user.email:
            return f'User-Email: {self.user.email} ' 
        else:
            return f'User-Email: {self.user.first_name} {self.last_name}'

#  create profile if user is sign up
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(
            user=instance, 
            first_name = instance.first_name,
            last_name = instance.last_name,
            email = instance.email,
            
        )
        user_profile.save()



