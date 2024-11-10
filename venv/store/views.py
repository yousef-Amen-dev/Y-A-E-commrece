from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .models import (Product,Category,Contact_Us)
from members.models import Profile
from .forms import (Add_Products_Form,Add_Category_Form,Contact_Us_Form)
from django.contrib import messages
from django.db.models import Q
from payment.models import OrderItem,Order
from django.db.models import Count,Sum
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction


# home page showing the products 
def home(request):
  context = {
    'products':Product.objects.all(),
    'categories':Category.objects.all(),
  }
  
  return render(request,'store/index.html',context)

# about the website inforamtions
def about(request):
  return render(request,'store/about.html')

# product details to show every product in sangle page
def product_details(request,slug):
  product = Product.objects.get(slug =slug)
  related_products = Product.objects.filter(category=product.category).exclude(slug=product.slug)
  context = {
    'product':product,
    'related_products':related_products,
    }
  return render(request,'store/product_details.html',context)


# the all categories and the all related products
def all_categories(requset):
  # get the all categories
  categories = Category.objects.all()
  # get the all products
  products = Product.objects.all()
  context  = {
    'categories': categories,
    'products':products
    }
  return render(requset,'store/all_categories.html',context)

# category and all products in singal page 
def category(request,cat):
  try:
    products = Product.objects.filter(category__name=cat)
    return render(request,'store/category.html',{'products':products,'category':cat})
  except Category.DoesNotExist:
    messages.info(request,"This Category Dose Not Exists...")
    return redirect('/')


# offers function 
def discount_products(request):
  products = Product.objects.filter(discount__gt=0)
  context = {'products':products}
  return render(request,'store/offers.html',context)


# add products function to can added products from the website only admins or staff can use this function
def add_products(request):
  if request.method == 'POST':
    # add the product info in the add_products form
    product_form = Add_Products_Form(request.POST,request.FILES)
    if product_form.is_valid():

      # save the products
      product_form.save()
      messages.success(request,'Product Add Successfully')
      return redirect('/')
    else:
      messages.info(request,'Product Is Not Add Please Chack The Product Informations And Try Agine..')
  product_form = Add_Products_Form()

  context = {'forms':product_form}

  return render(request,'store/add_products.html',context)


# update products page is display only if user is in staff
def update_products(request):
  products = Product.objects.all()
  context  = {'products':products}
  return render(request,'store/update_products.html',context)


# update products function only admins or staff can use this function 
def update_product(request,slug):
  product = Product.objects.get(slug=slug)
  if request.method == 'POST':
    form = Add_Products_Form(request.POST,request.FILES,instance=product)
    if form.is_valid():
      # save the the new informations in database
      form.save()
      messages.success(request,'Product Updated Successfully..')
      return redirect('/')
    else:
      messages.info(request,'Invalid Informations Please Chack The Product Detalis And Try Agine')
  form   = Add_Products_Form(instance=product)
  context= {'forms':form}
  return render(request,'store/update_product.html',context)


# delete products function onlay admins or staff can use this function 
def delete_products(request,slug):
  try:
    product = Product.objects.get(slug=slug)
    if request.method == "POST":
        # delete the product
        product.delete()
        messages.success(request,'Product Deleted Successfully..')
        return redirect('/')
    context = {'product':product}
    return render(request,'store/delete_products.html',context)
  except:
    meessages.info(request,'Error!')
    return redirect('/')


# add products function to can added products from the website only admins or staff can use this function
def add_categories(request):
  if request.method == "POST":
    category_form = Add_Category_Form(request.POST)
    if category_form.is_valid():
      # save the category in database
      category_form.save()
      messages.success(request,'Category Add Successfully')
      return redirect('/')
    else:
      messages.info(request,'Category Is Not Add Please Chack The Category Name And Try Agine..')
  category_form = Add_Category_Form()
  context = {'forms':category_form}
  return render(request,'store/add_categories.html',context)


# add products function to can added products from the website
def contact_us(request):
  user = request.user
  if request.method == 'POST' :
    if user.is_authenticated:
      # Use the transaction to ensure the complete success of the code, if there is any error the code will be defeated
      with transaction.atomic():
        contact_form = Contact_Us_Form(request.POST)
        if contact_form.is_valid():
          #  don't save the meesage before connect the meesage with the user
          contact = contact_form.save(commit=False)
          # connect the request user with the Contact US model to tell him the message related to this user
          contact.user = user
          contact.save()

          if request.user.profile.gender == 'Male':
            messages.success(request,f'Your Message Sended Successfully You Well Get The Answer Soon Mr {user.profile.first_name}')
          else:
            messages.success(request,f'Your Message Sended Successfully You Well Get The Answer Soon Miss {user.profile.first_name}')
          return redirect('/')
        else:
          messages.info(request,f'Your Message Not Sended Please Chack The Informations And Try Agine!')
    else:
      messages.info(request,'You Have To Sign Up First And Return To Send The Message!')
      return redirect('signup')
  contact_form = Contact_Us_Form()
  context = {'form':contact_form}
  return render(request,'store/contact_us.html',context)


def search_products(request):
  all_product  = Product.objects.all()
  if 'search_name' in request.GET:
    search_term = request.GET['search_name']

    if search_term:
      product = all_product.filter(Q(name__icontains = search_term) | Q(description__icontains = search_term) )
      if product:
        context = {'products':product}
        return render(request,'store/search_page.html',context)
      else:
        messages.info(request,f'Not Found {search_term}')
    return render(request,'store/search_error.html')


@login_required
def add_favourites_products(request):
  if request.POST.get('action') == 'post':
    user = request.user 
    product_id = int(request.POST.get('product_id'))
    product = get_object_or_404(Product,id =product_id)
    if product.favourites.filter(id =user.id).exists():
        product.favourites.remove(user)
        action = 'removed'
    else:
        product.favourites.add(user)
        action = 'added'
    product.save()
    return JsonResponse({'action': action})


# user favourite page the display user favourite products 
def user_favourites_products_page(request):
  user  = request.user
  fav_products = Product.objects.filter(favourites=user )
  context = {'fav_products':fav_products}
  return render(request,'store/user_favourties_products.html',context)


# to remove products from user favourite products 
def remove_favourite_product(request,slug):
  if request.method == "POST":
    product = get_object_or_404(Product, slug=slug)

    user  = request.user
    # check if user is already liked the product 
    if product.favourites.filter(id = user.id).exists():
      # remove the product from user favourite products
      product.favourites.remove(user)
      messages.success(request,'Product Removed From Your Favourite Products Successfully.')
    else:
      messages.error(request, 'Product is not in your favourites.')
    return redirect('/')


def popular_products(request,num_products=10):
  # get the products id and use the annotate function to add likes_count filed to count favourites 
  products_with_id = Product.objects.values('id').annotate(likes_count = Count('favourites')).order_by('-likes_count')[:num_products]
  print(products_with_id)
  # extract the products ids in list
  extract_products = products_with_id.values_list('id',flat = True)
  products = Product.objects.filter(id__in=extract_products) \
    .annotate(likes_count=Count('favourites')) \
    .order_by('-likes_count')[:num_products]
  print(products)
  context  = {'products':products}
  return render(request,'store/popular_products.html',context)


def most_sold_products(request, num_products=10):
  # get the product ids with quantity and order him total_quantity the most sold product will be appear first
  product_ids_with_quantity = OrderItem.objects.values('products_id')  \
    .annotate(total_quantity=Sum('quantity')) \
    .order_by('-total_quantity')[:num_products]
  # extract the products ids from product_ids_with_quantity and add him flat list,flat=True  makes sure result is list not list of tuples.
  product_ids = product_ids_with_quantity.values_list('products_id', flat=True)
  # filters the products where the id is in list of product_ids and 
  # return sums the total of product quantity using the related_name of the model (orderitem_quantity) 
  # and order him again the most sold product is well be the first
  products = Product.objects.filter(id__in=product_ids) \
    .annotate(total_quantity=Sum('orderitem__quantity')) \
    .order_by('-total_quantity')
  return render(request, 'store/most_selld_product.html', {'products':products,})


def mark_as_shipped(request):
  if request.method == "POST"  and request.user.is_authenticated and request.user.is_superuser:
    try :
      order_uuid = request.POST.get('order-button')
      order = Order.objects.get(order_uuid = order_uuid)
      order.shipped = True
      order.save()
      messages.success(request, 'Order marked as shipped successfully.')
      return redirect('shipped_orders_dashboard')
    except order.DoseNotExist:
      messages.success(request, 'Order marked as shipped successfully.')
      return redirect('shipped_orders_dashboard')
  messages.error(request, 'You do not have permission to perform this action.')
  return redirect('login') if not request.user.is_authenticated else redirect('/')
