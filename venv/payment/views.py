from django.shortcuts import render,redirect
from .forms import (ShippingAddressForms,AddShippingAddress,PaymentForm)
from django.contrib import messages
from cart.cart import Cart
from .models import (Order,OrderItem)
from .models import (ShippingAddress)
from django.contrib.auth.decorators import login_required
from store.models import Product
from members.models import Profile
from decimal import Decimal
from django.db import transaction


def chackout(request):
  # get the cart
  cart = Cart(request)
  products = cart.get_products()
  quantity = cart.get_quantitys()  
  total = cart.total_price()
  context = {'cart_products':products,'quantity':quantity,'total_price':total}
  return render(request,'payment/chackout.html',context)


def chackout_shipping_address(request):
  if request.user.is_authenticated:
    user_shipping_address = ShippingAddress.objects.filter(user= request.user.id)
    if user_shipping_address.exists():
      context = {'shipping_addresses':user_shipping_address,'orders':Order.objects.all()}
      return render(request,'payment/choose_shipping_address.html',context)
    else:
      messages.warning(request,'You Dont Have Any Address,Please Add One.')
    return render(request,'payment/choose_shipping_address.html',)
  else:
    messages.warning(request,'Should Be Login First To Continue Order Proccess.')
    return redirect('login')


def user_shipping_addresses(request):
  shipping_addresses = ShippingAddress.objects.filter(user =request.user)
  if shipping_addresses.exists():
    context = {'shipping_addresses':shipping_addresses,}
    return render(request,'members_pages/user_shipping_addresses.html',context)
  else:
    messages.warning(request,'You Dont Have Any Address,Please Add One.')
    return render(request,'payment/user_shipping_addresses.html',)


def add_shippingAddress(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      form = AddShippingAddress(request.POST)
      if form.is_valid():
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.shipping_email = request.user.email
        shipping_address.save()
        messages.success(request,'The Shipping Address Is Added Successfully..')
        return redirect('user_shipping_addresses')
      else:
        for error in list(form.errors.values()):
          messages.error(request,error) 
    form = AddShippingAddress()
    return render(request,'store/add_shipping_address.html',{'form':form})
  else:
    messages.warning(request,'You Have To Login First To Can Add Address.')
    return redirect('login')


def update_shipping_address(request,token):
  try:
      address = ShippingAddress.objects.get(token=token)
      if request.method == 'POST':
        form = ShippingAddressForms(request.POST , instance = address)
        if form.is_valid():
          form.save()
          messages.success(request,'Address Updated Successfully.')
          return redirect('chackout_shipping_address')
        else:
          for error in list(form.errors.values()):
            messages.error(request,error) 
      form = ShippingAddressForms(instance = address)
      context = {'form':form}
      return render(request,'store/update_address.html',context)
  except Exception as error:
    return render(request,'store/unavalable_page.html')


def delete_shipping_address(request,token):
  try:
    address = ShippingAddress.objects.get(token=token)
    if request.method == "POST":
      address.delete()
      messages.success(request,'Address Delete Successfully.')
      return redirect('chackout_shipping_address')
    return render(request,'store/delete_shipping_address.html',{'address':address})

  except ShippingAddress.DoesNotExist:
    messages.error(request, 'Address Not Found.')
    return redirect('chackout_shipping_address')


def order_process(request, token):
    if request.user.is_authenticated:
        cart = Cart(request)
        total = float(cart.total_price())
        products = cart.get_products()
        quantity = cart.get_quantitys()
        
        try:
            shipping_address = ShippingAddress.objects.get(token=token)
            shipping_address_summary = (
                f"{shipping_address.shipping_full_name}\n"
                f"{shipping_address.shipping_email}\n"
                f"{shipping_address.shipping_address1}\n"
                f"{shipping_address.shipping_address2}\n"
                f"{shipping_address.shipping_phone}\n"
                f"{shipping_address.building_name}\n"
                f"{shipping_address.shipping_state}\n"
                f"{shipping_address.shipping_city}\n"
                f"{shipping_address.shipping_zipcode}\n"
                f"{shipping_address.shipping_country}"
            )
          
            order = Order(
                shipping_address=shipping_address,
                user=request.user,
                amount=total,
                email=shipping_address.shipping_email,
                full_name=shipping_address.shipping_full_name,
                summary_shipping_address=shipping_address_summary
            )
            # Store order details in session as a dictionary (not as an object)
            request.session['order_data'] = {
                'shipping_address_id': shipping_address.id,
                'user_id': request.user.id,
                'amount': total,
                'email': shipping_address.shipping_email,
                'full_name': shipping_address.shipping_full_name,
                'summary_shipping_address': shipping_address_summary
            }
            
            context = {'order':order,'cart_products': products, 'quantity': quantity}
            return render(request, 'payment/order_details.html', context)
        
        except ShippingAddress.DoesNotExist:
            messages.error(request, 'Invalid Shipping Address.')
            return redirect('checkout')
    else:
        messages.warning(request, 'You must be logged in to proceed with payment.')
        return redirect('login')


def billing_info(request):
    if request.user.is_authenticated:
        cart = Cart(request)
        total = cart.total_price()
        products = cart.get_products()
        quantity = cart.get_quantitys()

        if request.method == "POST":
            try:
                # Retrieve the order data from session
                with transaction.atomic():
                  order_data = request.session.get('order_data')
                  if not order_data:
                      messages.error(request, 'Order not found. Please start the order process again.')
                      return redirect('checkout')

                  # Create and save the order instance
                  order = Order.objects.create(
                      shipping_address_id=order_data['shipping_address_id'],
                      user_id=order_data['user_id'],
                      amount=order_data['amount'],
                      email=order_data['email'],
                      full_name=order_data['full_name'],
                      summary_shipping_address=order_data['summary_shipping_address']
                  )

                  # Create OrderItems for each product in the cart
                  for product in products:
                      product_quantity = quantity.get(str(product.id), 0)
                      if product_quantity > 0:
                          OrderItem.objects.get_or_create(
                              order=order,
                              products=product,
                              user=request.user,
                              price=product.price,
                              quantity=product_quantity
                          )
                  
                  # Clear the session and cart
                  for key in list(request.session.keys()):
                    if key == "session_key":
                      del request.session[key]
                  Profile.objects.filter(user=request.user).update(cart="")
                  
                messages.success(request,f'Order Pleced Successfully {request.user.profile.first_name}.')
                return redirect('/')
            
            except Exception as error:
                messages.info(request, f'Order not placed. Please try again: {error}')
                return redirect('/')

        billing_forms = PaymentForm()
        context = {'payment_form': billing_forms}
        return render(request, 'payment/billing_info.html', context)
    else:
        messages.warning(request, 'You must be logged in to proceed with payment.')
        return redirect('login')


def user_orders(request):
  filter_user_orders=Order.objects.filter(user=request.user)
  context = {'user_orders':filter_user_orders,}
  return render(request,'payment/user_orders.html',context)


def user_orders_detail(request,order_uuid):
  order=Order.objects.get(order_uuid=order_uuid)
  orderitem = OrderItem.objects.filter(order=order.id)
  context = {'order':order,'orderitem':orderitem}
  return render(request,'payment/user_orders_detail.html',context)


def cancel_order(request,order_uuid):
  try:
    order = Order.objects.get(order_uuid = order_uuid)
    orderitem = OrderItem.objects.filter(order=order.id)
    if not order.shipped:
      if request.method == 'POST':
        order.delete()
        messages.success(request,'Order Cancel Successfully.')
        return redirect('user_orders')
      context = {'order':order,'orderitem':orderitem}
      return render(request,'payment/cancel_order.html',context)
    else:
      messages.info(request,"Order Can't Cancel This Order Is Shipped.")
      return redirect('user_orders')
  except Exception as error:
    messages.error(request,f'{error}')


def payment_process(request):
  if request.user.is_authenticated:
    billing_forms = PaymentForm(request.POST or None)
    return render(request, 'payment/payment_page.html')
  else:
    messages.warning(request,'Access Is Denied')
    return redirect('/')


def shipped_orders_dashboard(request):
  orders = Order.objects.filter(shipped= True)
  context  = {'shipped_orders':orders}
  return render(request,'payment/shipped_orders_dashboard.html',context)


def unshipped_orders_dashboard(request):
  orders = Order.objects.filter(shipped= False)
  context  = {'unshipped_orders':orders}
  return render(request,'payment/unshipped_orders_dashboard.html',context)


