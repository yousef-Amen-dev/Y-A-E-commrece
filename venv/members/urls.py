from django.urls import path
from .views import(signup_user,
  login_user,logout_user,
  update_profile,profile,update_password
  )
urlpatterns  = [
  path('signup/',signup_user,name='signup'),
  path('login/',login_user,name='login'),
  path('logout/',logout_user,name='logout'),
  path('profile/',profile,name='profile'),
  path('profile/update',update_profile ,name = 'update_profile'),
  path('update_password/',update_password,name= 'update_password')
] 

