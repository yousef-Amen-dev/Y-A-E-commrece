from django import forms
from .models import (Product,Category,Contact_Us)

# Add_Products_Form forms
class Add_Products_Form(forms.ModelForm):
  class Meta:
    model   = Product
    fields  = ['product_model','name','image','image_two','image_three','image_foure','description','price','discount','instock','category']
    widgets = {
      'product_model':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter The Product Brand Name (Must Contain At Least 3 Character)'}),
      'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter The Product Name (Must Contain At Least 3 Character)'}),
      'image':forms.FileInput(attrs={'class':'form-control'}),
      'image_two':forms.FileInput(attrs={'class':'form-control','placeholder':'Optional'}),
      'image_three':forms.FileInput(attrs={'class':'form-control','placeholder':'Optional'}),
      'image_foure':forms.FileInput(attrs={'class':'form-control','placeholder':'Optional'}),
      'description':forms.Textarea(attrs={'class':'form-control','placeholder':'About The Product (Must Contain At Least 10 Character)'}),
      'price':forms.NumberInput(attrs={'class':'form-control',}),
      'discount':forms.NumberInput(attrs={'class':'form-control',}),
      'instock':forms.NumberInput(attrs={'class':'form-control'}),
      'category':forms.Select(attrs={'class':'form-control','placeholder':'Enter Product Name'}),
      
    }
    class Meta:
      model = Product
      exclude = ['favourites']

# Add_Category_Form forms
class Add_Category_Form(forms.ModelForm):
  class Meta:
    model   = Category
    fields  = ['name']
    widgets = {
      'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter The Name Of Category'}),
    }


# contact us forms
class Contact_Us_Form(forms.ModelForm):
  class Meta:
    model   = Contact_Us
    fields  = ['name','email','message']
    widgets = {
      'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Name'}),
      'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}),
      'message':forms.Textarea(attrs={'class':'form-control','placeholder':'Enter The Message'})
    }