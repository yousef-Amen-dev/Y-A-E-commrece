from django import forms
from .models import (ShippingAddress,COUNTRIES)


# Shipping Address Forms
class ShippingAddressForms(forms.ModelForm):
  class Meta :
    model  = ShippingAddress
    fields = ['shipping_full_name','shipping_email','shipping_address1','shipping_address2','shipping_phone','shipping_city','shipping_state','building_name','shipping_zipcode','shipping_country']
    widgets = {
      'shipping_full_name':forms.TextInput(attrs = {'class':'form-control','placeholder':'Full Name'}),
      'shipping_email':forms.EmailInput(attrs = {'class':'form-control','placeholder':'Email'}),
      'shipping_address1':forms.TextInput(attrs = {'class':'form-control','placeholder':'Address One'}),
      'shipping_address2':forms.TextInput(attrs = {'class':'form-control','placeholder':'Address Two'}),
      'building_name':forms.TextInput(attrs = {'class':'form-control','placeholder':'Building Name'}),
      'shipping_phone':forms.TextInput(attrs = {'class':'form-control','placeholder':'Phone Number'}),
      'shipping_city':forms.TextInput(attrs = {'class':'form-control','placeholder':'City'}),
      'shipping_state':forms.TextInput(attrs = {'class':'form-control','placeholder':'State'}),
      'shipping_zipcode':forms.TextInput(attrs = {'class':'form-control','placeholder':'Zipcode'}),
      'shipping_country':forms.Select(attrs = {'class':'form-control','placeholder':'Country'}),
    }

class AddShippingAddress(forms.ModelForm):
  class Meta:
    model  = ShippingAddress
    fields = ['shipping_full_name','shipping_address1','shipping_address2','shipping_phone','shipping_city','shipping_state','shipping_zipcode','shipping_country']

    widgets = {
      'shipping_full_name':forms.TextInput(attrs = {'class':'form-control','placeholder':'Full Name'}),
      # 'shipping_email':forms.EmailInput(attrs = {'class':'form-control','placeholder':'Email'}),
      'shipping_address1':forms.TextInput(attrs = {'class':'form-control','placeholder':'Address One'}),
      'shipping_address2':forms.TextInput(attrs = {'class':'form-control','placeholder':'Address Two'}),
      'shipping_phone':forms.TextInput(attrs = {'class':'form-control','placeholder':'Phone Number'}),
      'shipping_city':forms.TextInput(attrs = {'class':'form-control','placeholder':'City'}),
      'shipping_state':forms.TextInput(attrs = {'class':'form-control','placeholder':'State'}),
      'shipping_zipcode':forms.TextInput(attrs = {'class':'form-control','placeholder':'Zipcode'}),
      'shipping_country':forms.Select(attrs = {'class':'form-control','placeholder':'Country'}),
    }


class PaymentForm(forms.Form):
  card_name        = forms.CharField(label='', required=True,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name On Card'}))
  card_number      = forms.CharField(label ='', required = True,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}))
  card_exp_date    = forms.CharField(label ='',required = True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Expiration Date'}))
  card_cvv_number  = forms.CharField(label ='',required = True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'CVV Code'}))
  card_address1    = forms.CharField(label ='',required = True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing Adddress 1'}))
  card_address2    = forms.CharField(label ='',required = False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing Adddress 2'}))
  card_city        = forms.CharField(label ='',required = True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing City'}))
  card_state       = forms.CharField(label ='',required = True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing State'}))
  card_zipcode     = forms.CharField(label ='',required = True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Billing ZipCode'}))
  card_country     = forms.ChoiceField(choices=COUNTRIES, label='', required=True, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Billing Country'}))







