from django.urls import path
from .views import (
  home,most_sold_products,product_details,
  category,all_categories,add_categories,add_products,
  update_products,update_product,delete_products,
  contact_us,search_products,discount_products,about,add_favourites_products,
  user_favourites_products_page,remove_favourite_product, popular_products,mark_as_shipped
)
urlpatterns  = [
  path('', home, name='home'),
  path('About Us/',about,name='about'),
  path('product details/<slug:slug>',product_details,name='product_details'),
  path('product/<str:cat>/',category,name='category'),
  path('categories',all_categories,name='all_categories'),
  path('add_products/',add_products,name='add_products'),
  path('update_products/',update_products,name='update_products'),
  path('update_products/update/<slug:slug>/product/',update_product,name='update_product'),
  path('update_products/delete/<slug:slug>/product/',delete_products,name='delete_products'),
  path('add_categories/',add_categories,name='add_categories'),
  path('contact_us/',contact_us,name='contact_us'),
  path('search/',search_products,name='search_products'),
  path('offers/',discount_products,name='offers_product'),
  path('most_selled_products/',most_sold_products, name = 'most_selled_products'),
  path('user_favourites_products_page/',user_favourites_products_page, name = 'user_favourites_products_page'),
  path('add_favourites_products/',add_favourites_products, name = 'add_favourites_products'),
  path('remove_favourite_product/remove/<str:slug>',remove_favourite_product, name = 'remove_favourite_product'),
  path('popular_products/',popular_products,name = 'popular_products'),
  path('mark_as_shipped/',mark_as_shipped,name = 'mark_as_shipped')
] 
