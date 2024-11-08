from django.contrib import admin
from .models import (ShippingAddress,Order,OrderItem)

# registering the models
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


class OrderItemInline(admin.StackedInline):
  model   = OrderItem
  extra   = 0
  fields  = ['products','quantity','price',] 


class OrderAdmin(admin.ModelAdmin):
  model           = Order
  readonly_fields = ['order_time']
  inlines         = [OrderItemInline,]

# unregister the models
admin.site.unregister(Order)
# re-register the models
admin.site.register(Order,OrderAdmin)