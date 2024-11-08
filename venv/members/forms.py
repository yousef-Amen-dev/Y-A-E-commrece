from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from .models import Profile
GENDER_CHOICES = (
    ('Male','Male'),
    ('Female','Female'),
)


class SignUpForm(UserCreationForm):
	email 			= forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name 	= forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name 	= forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	gender 			= forms.ChoiceField(choices = GENDER_CHOICES,label="",widget=forms.Select(attrs = {'class':'form-control', 'placeholder':'Gender'}))
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name','email','gender', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class UserProfileForm(forms.ModelForm):
	class Meta:
		model  	= Profile
		fields  = ['first_name','last_name','email','gender','profile_image','phone','address','state','city','zipcode','country',]
		widgets = {
			'first_name':forms.TextInput(attrs = {'class':'form-control','placeholder':'Firt Name'}),
			'last_name':forms.TextInput(attrs = {'class':'form-control','placeholder':'Last Name'}),
			'email':forms.TextInput(attrs = {'class':'form-control','placeholder':'Email'}),
			'gender':forms.Select(attrs = {'class':'form-control','placeholder':'gender'}),
			'profile_image':forms.FileInput(attrs={'class':'form-control'}),
			'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Phone Number'}),
			'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Adderss'}),
			'state':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your State'}),
			'city':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your City'}),
			'zipcode':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your City'}),
			'country':forms.Select(attrs={'class':'form-control','placeholder':'Enter Your Countery'}),
		} 

class ChangePasswordForm(PasswordChangeForm):
		def __init__(self, *args, **kwargs):
			super(PasswordChangeForm, self).__init__(*args, **kwargs)

			self.fields['old_password'].widget.attrs['class'] = 'form-control'
			self.fields['old_password'].widget.attrs['placeholder'] = 'Enter The Old Password'
			self.fields['old_password'].label = ''

			self.fields['new_password1'].widget.attrs['class'] = 'form-control'
			self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter The New Password'
			self.fields['new_password1'].label = ''
			self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

			self.fields['new_password2'].widget.attrs['class'] = 'form-control'
			self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
			self.fields['new_password2'].label = ''
			self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
		def clean_new_password1(self):
			new_password = self.cleaned_data['new_password1']
			if len(new_password) < 8:
				raise ValidationError('The Password Must be Greater Than 8 characters ')
			return new_password