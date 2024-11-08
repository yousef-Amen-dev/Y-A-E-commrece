from django.urls import path
from .views import *
urlpatterns =[
  path('',summary_cart,name='summary_cart'),
  path('add_cart/',add_cart,name='add_cart'),
  path('update_cart/',update_cart,name='update_cart'),
  path('delete_cart/',delete_cart,name='delete_cart'),
  path('clear_cart/',clear_cart_views,name='clear_cart'),
]