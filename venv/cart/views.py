from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from store.models import Product,Category
from django.http import JsonResponse
from members.models import Profile
from django.contrib import messages


# summary cart function
def summary_cart(request):
  # get the cart
  cart = Cart(request)
  products = cart.get_products
  all_products= Product.objects.all()
  # get the quantitys of the products
  get_quantity = cart.get_quantitys
  if request.user.is_authenticated:
    profile = request.user.profile
  else:
    profile = None
  total = cart.total_price()

  category =Category.objects.all()
  
  context = {
  'cart_products':products,
  'products':all_products,
  'categories':category,
  'profile':profile,
  'product_quantitys':get_quantity,
  'total':total
  }
  return render(request,'cart/summary_page.html',context)


# view cart function
def view_cart(request):
  return render(request,'cart/update.html',context)


# add cart function
def add_cart(request):
  # get the Cart Class
  cart = Cart(request)
  #  chack if the action is equal post
  if request.POST.get('action') == 'post':
    # lookup products in database
    product_id = int(request.POST.get('product_id'))
    # get the cart quantity
    product_qty = int(request.POST.get('product_qty'))
    # get the products from the Product model
    product    = get_object_or_404(Product,id=product_id)
    # save the session 
    cart.add(product=product,product_qty=product_qty)
    # get the cart products length
    cart_qty = cart.__len__()
    # return response
    response = JsonResponse({'qty':cart_qty,'product name':product.name})
    return response


# delete function to delete products from the cart cart
def delete_cart(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    #  get the product id from the template
    product_id =int(request.POST.get('product_id'))
    # call delete fucntion from cart
    cart.delete(product = product_id)
    # return response
    response = JsonResponse({'product':product_id})
    return response
    return redirect('summary_cart')


# update products in cart
def update_cart(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    # get the product id
    product_id =int( request.POST.get('product_id'))
    # get the quantity
    product_qty = int(request.POST.get('product_qty'))
    # update the cart
    cart.update(product=product_id,product_qty = product_qty)
    response = JsonResponse({'qty':product_qty})
    return response
    return redirect('summary_cart')


def clear_cart_views(request):
  cart = Cart(request)
  if request.method == 'POST':
    cart.clear_cart()
    messages.success(request,'Cart Is Clear Successfully.')
    return redirect('/')