import datetime
import uuid
from django.db import models
from django.contrib.auth.models import User
from members.models import Profile
from django.core.validators import MinLengthValidator
from django.template.defaultfilters import slugify

class Category(models.Model):
  name                = models.CharField(max_length =500,default=None,verbose_name='Category Name',validators=[
    MinLengthValidator(3,'the field must contain at least 20 character')
  ])

  class Meta:
    verbose_name_plural = 'Categories'

  def __str__(self):
    return self.name


class Product(models.Model):
  product_model        = models.CharField(max_length =1000,default=None,validators=[
    MinLengthValidator(3,'the field must contain at least 3 character')],null=True,blank=True,verbose_name='Product Brand')
  name                = models.CharField(max_length =1500,default=None,verbose_name='Product Name',validators=[
    MinLengthValidator(2,'the field must contain at least 2 character')
  ])
  image               = models.ImageField(upload_to ='images/products_images/', verbose_name='Product Image')
  image_two           = models.ImageField(upload_to ='images/products_images/related_images',null=True,blank=True,verbose_name='Product Image')
  image_three         = models.ImageField(upload_to ='images/products_images/related_images',null=True,blank=True,verbose_name='Product Image')
  image_foure         = models.ImageField(upload_to ='images/products_images/related_images',null=True,blank=True,verbose_name='Product Image')
  description         = models.TextField(max_length =1500,default =None,null=True,blank=True,validators=[
    MinLengthValidator(10,'the field must contain at least 10 characters')
  ])
  price               = models.DecimalField(max_digits=8,decimal_places=2,default=0,verbose_name='Product Price')  
  discount            = models.DecimalField(max_digits=8,decimal_places = 2,default=0,null=True,blank=True,verbose_name='Dicount')
  category            = models.ForeignKey(Category,on_delete=models.CASCADE,default=1,verbose_name='Category')
  instock             = models.IntegerField(default = 1)
  favourites          = models.ManyToManyField(User, blank=True,)
  slug                = models.SlugField(null=True,blank = True,max_length=1500) 
  added               = models.DateTimeField(auto_now_add=True)

  # make the discount auto and save
  def save(self,*args,**kwargs):
    if self.discount:
      self.price -= self.discount
    self.slug = slugify(self.name )
    super(Product,self).save(*args,**kwargs)
  
  def __str__(self):
    return self.name


class Contact_Us(models.Model):
  name          = models.CharField(max_length=50,default=None)
  email         = models.EmailField(max_length=100,default=None)
  message       = models.TextField(max_length=250,default=None)
  user          = models.ForeignKey(User,on_delete=models.CASCADE)

  class Meta:
    verbose_name_plural = 'Contact Us'
  
  def __str__(self):
    return self.email
