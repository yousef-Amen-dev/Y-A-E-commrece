from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from store.models import Product,Category
from django.http import JsonResponse
from members.models import Profile
from django.contrib import messages


def summary_cart(request):
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


def view_cart(request):
  return render(request,'cart/update.html',context)


def add_cart(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    # lookup products in database
    product_id = int(request.POST.get('product_id'))
    product_qty = int(request.POST.get('product_qty'))
    product    = get_object_or_404(Product,id=product_id)
    cart.add(product=product,product_qty=product_qty)
    cart_qty = cart.__len__()
    response = JsonResponse({'qty':cart_qty,'product name':product.name})
    return response


# delete function to delete products from the cart cart
def delete_cart(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    product_id =int(request.POST.get('product_id'))
    cart.delete(product = product_id)
    response = JsonResponse({'product':product_id})
    return response
    return redirect('summary_cart')


def update_cart(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    # get the product id and product quantity
    product_id =int( request.POST.get('product_id'))
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