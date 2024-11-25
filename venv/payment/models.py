from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from store.models import Product
import uuid
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import datetime
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


class ShippingAddress(models.Model):
  user               = models.ForeignKey(User,on_delete = models.CASCADE,null = True, blank  = True)
  shipping_full_name = models.CharField(max_length = 255,)
  shipping_email     = models.EmailField(max_length = 50,default = None,null = True,blank=True)
  shipping_address1  = models.CharField(max_length = 400,default = None, verbose_name = 'Address' )
  shipping_address2  = models.CharField(max_length = 400,default = None, verbose_name = 'Address' )
  building_name      = models.CharField(max_length = 400,default = None, verbose_name = 'Building Name',null=True)
  shipping_phone     = models.CharField(max_length=11,default = None,validators = [
        MinLengthValidator(11,'The Field Must be contain 11 Numbers')
    ])
  shipping_city      = models.CharField(max_length = 255,blank = True)
  shipping_state     = models.CharField(max_length = 255,blank = True)
  shipping_zipcode   = models.CharField(max_length = 255,blank = True)
  shipping_country   = models.CharField(max_length=255, blank=True, choices=COUNTRIES, default='US')

  token              = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  class Meta:
    verbose_name_plural = 'Shipping Address'

  def __str__(self):
    return f"""
    {self.shipping_full_name}
    \n{self.shipping_email}
    \n{self.shipping_address1}
    \n{self.shipping_address2}
    \n{self.shipping_phone}
    \n{self.building_name}
    \n{self.shipping_state}
    \n{self.shipping_city}
    \n{self.shipping_zipcode}
    \n{self.shipping_country}"""


class Order(models.Model):
  user                     = models.ForeignKey(User,on_delete = models.CASCADE,null=True,blank=True,related_name = 'orders')
  full_name                = models.CharField(max_length = 250) 
  email                    = models.EmailField(max_length = 250) 
  shipping_address         = models.ForeignKey(ShippingAddress,on_delete=models.CASCADE,)
  summary_shipping_address = models.TextField(max_length = 15000,default=None)
  amount                   = models.DecimalField(max_digits =7,decimal_places = 2)
  shipped                  = models.BooleanField(default =False)
  date_shipped             = models.DateTimeField(blank = True ,null = True)
  order_time               = models.DateTimeField(auto_now_add=True)
  order_uuid               = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  def __str__(self):
    return f'Order-Email : {self.email}'

# add the date time when the product marked as shipped
@receiver(pre_save, sender=Order)
def set_shipped_date(sender,instance,**kwargs):
  if instance.pk and instance.shipped:
    instance.date_shipped = datetime.datetime.now()


class OrderItem(models.Model):
  order             = models.ForeignKey(Order,on_delete = models.CASCADE,null=True)
  products          = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
  user              = models.ForeignKey(User,on_delete = models.CASCADE,null=True,blank=True)
  quantity          = models.PositiveIntegerField(null=True)
  price             = models.DecimalField(max_digits = 7, decimal_places = 2)
  
  def __str__(self):
    return f'Product : {self.products.name if self.products else "No Product"}' 


