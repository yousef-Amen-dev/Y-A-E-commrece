# Imports
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from .forms import (SignUpForm,UserProfileForm,ChangePasswordForm)
from .models import Profile
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import json
from django.db import transaction


def signup_user(request):
  try:
    form = SignUpForm()
    if request.method == "POST":
      form = SignUpForm(request.POST)
      if form.is_valid():
        with transaction.atomic():
          user = form.save(commit=False)
          user.gender = request.POST.get('gender')
          user.save()
          login(request, user)
        messages.success(request, f'Account created successfully. Welcome {request.user.first_name}👋,Please Fill Out Your Information..') 
        return redirect('update_profile')
      else:
        for error in list(form.errors):
          messages.info(request,f'Please Chack Your Information And Try Agine {error}')
        return render(request,'members_pages/signup.html',{'form':form})
    form = SignUpForm()
    context = {'form':form}
    return render(request,'members_pages/signup.html',context)
  except ValueError as error:
    messages.error(request,f'Invalid Value {error}')
    return redirect('signup')
  except Exception as ex_error:
    if "UNIQUE constraint failed" in str(ex_error):
      messages.error(request, 'This email is already registered. Please try another email.')
    else:
      messages.error(request, 'An unexpected error occurred. Please try again later.')
    return redirect('signup')


def login_user(request):
  try:
    if request.method == "POST":
      date = request.POST
      user = authenticate(request,username =date['username'],password=date['password'])
      if user is not None:
        login(request,user)
        current_user = Profile.objects.get(user__id = request.user.id ) 
        saved_cart = current_user.cart
        if saved_cart:
          # convert database string to python dictionary using JSON
          convert_cart = json.loads(saved_cart)
          cart = Cart(request)
          for key,value in convert_cart.items():
            cart.db_add(product = key,product_qty = value)
        
        messages.success(request,f'Login successful. Welcome back, {user.username}!')
        return redirect('/')
      else:
        messages.error(request, 'Invalid credentials. Please try again.')
    return render(request,'members_pages/login.html')
  except Exception as error:
    messages.error(request,error)
    return redirect('/')


def logout_user(request):
  logout(request)
  messages.success(request,'Logout successful.')
  return redirect('/')


@login_required
def profile(request):
  try:
    if request.user.profile:
      profile = request.user.profile
      return render(request,'members_pages/user_profile.html',{'profile':profile})
    else:
      messages.info(request, "Sorry, you don't have an account. Please sign up again.")
      return redirect('signup')
  except Exception as error:
    messages.error(request, f"An error occurred: {error}")
    return redirect('/')
  except DoesNotExist as error:
    messages.error(request,error)



@login_required
def update_profile(request):
  try:
      profile = request.user.profile
      if request.method == "POST":
          form = UserProfileForm(request.POST,request.FILES, instance=profile)
          if form.is_valid():
            form.save()
            messages.success(request, f'Profile Is Updated Successfully {request.user.first_name}.')
            return redirect("profile")
          else:
            messages.info(request, 'Invalid Information ! Please Chack Your Details.')
      else:
        form = UserProfileForm(instance=profile)
      context = {'forms': form}
      return render(request, 'members_pages/update_profile.html', context)
  except:
    messages.error(request,'This Account is Not Defined Please Sign up Agine..')
    return redirect('/')


@login_required
def update_password(request):
  try:
    if request.method == 'POST':
        form = ChangePasswordForm(user =request.user,data=request.POST)
        if form.is_valid():
          form.save()
          update_session_auth_hash(request, form.user)
          messages.success(request,f'Password Is Updated Successfully..')
          return redirect('/') 
        for error in list(form.errors.values()):
          messages.error(request,error) 
    else:
      form = ChangePasswordForm(user =request.user)
    return render(request,'members_pages/update_password.html',{'form':form})
  except Exception as error:
    messages.error(request, f"An error occurred: {error}")
    return redirect('/')


