from django.urls import path
from .views import  (
  chackout,payment_process,billing_info,user_orders_detail,shipped_orders_dashboard,
  chackout_shipping_address,add_shippingAddress,user_orders,cancel_order,unshipped_orders_dashboard,
  update_shipping_address,delete_shipping_address,order_process,user_shipping_addresses
  )


urlpatterns = [
  path('user_shipping_addresses/',user_shipping_addresses,name = 'user_shipping_addresses'),
  path('orders/',user_orders,name = 'user_orders'),
  path('user_order_detail/?=<str:order_uuid>',user_orders_detail,name = 'user_order_detail'),
  path('cancel_order/?=<str:order_uuid>',cancel_order,name = 'cancel_order'),
  path('chackout/',chackout,name = 'chackout'),
  path('chackout/shipping_address/',chackout_shipping_address,name = 'chackout_shipping_address'),
  path('add_shipping_address/',add_shippingAddress,name = 'add_shipping_address'),
  path('update_shipping_address/<str:token>/',update_shipping_address,name = 'update_shipping_address'),
  path('delete_shipping_address/<str:token>/',delete_shipping_address,name = 'delete_shipping_address'),
  path('order_process=?<str:token>/',order_process, name = 'order_process'),
  path('billing_info/',billing_info, name = 'billing_info'),
  path('payment_process/',payment_process, name = 'payment_process'),
  # shipped and unshipped page for the admin 
  path('shipped_orders_dashboard/',shipped_orders_dashboard,name = 'shipped_orders_dashboard'),
  path('unshipped_orders_dashboard/',unshipped_orders_dashboard,name = 'unshipped_orders_dashboard'),
  

]
