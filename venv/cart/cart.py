# imports
from store.models import Product
from members.models import Profile
class Cart():

  def __init__(self,request):
    self.session = request.session
    self.request = request
    cart = self.session.get('session_key')
    # create session if user is new
    if 'session_key' not in request.session:
      cart = self.session['session_key'] = {}
    self.cart = cart


  def db_add(self, product, product_qty):
    product_id = str(product)
    product_qty = int(product_qty)

    # Logic
    if product_id in self.cart:
      pass
    else:
        # self.cart[product_id] = {'price': str(product.price)}
        self.cart[product_id] = int(product_qty)

    self.session.modified = True

    if self.request.user.is_authenticated:
        # Get the current user profile
        current_user = Profile.objects.filter(user__id=self.request.user.id)

        carty = str(self.cart)
        carty = carty.replace("\'", "\"")
        # Save carty to the Profile Model
        current_user.update(cart=str(carty))


  # add product in cart
  def add(self,product,product_qty):
    # get the product id
    product_id = str(product.id)
    # get the product quantity
    product_qty = int(product_qty)
    # chack if product id in the cart
    if product_id not in self.cart:
      # self.cart[product_id] = {'price':str(product.price)}
      self.cart[product_id] = int(product_qty)
    # update the session
    self.session.modified = True

    if self.request.user.is_authenticated:

      current_user = Profile.objects.filter(user__id = self.request.user.id)
      # convert the single quteion to duble quteion
      carty =str(self.cart)
      carty=carty.replace("\'","\"")
      current_user.update(cart = str(carty))


  # get the products in the cart
  def get_products(self):
    products_ids = self.cart.keys()
    # useing the ids to lookeup products in the database
    products = Product.objects.filter(id__in=products_ids)
    return products

  def __len__(self):
    return len(self.cart)

  def get_quantitys(self):
    quantity = self.cart
    return quantity
  

  def update(self,product,product_qty):
    # get the product id
    product_id = str(product)
    # get the product quantity
    product_qty = int(product_qty)
    cart = self.cart
    cart[product_id] = product_qty
    # update the session
    self.session.modified = True
    if self.request.user.is_authenticated:

      current_user = Profile.objects.filter(user__id = self.request.user.id)
      # convert the single quteion to duble quteion
      carty =str(self.cart)
      carty=carty.replace("\'","\"")
      current_user.update(cart = str(carty))

    new_cart = self.cart
    return new_cart 


  def delete(self,product):
    # get the product id
    product_id = str(product)
    # delete product from  cart
    if product_id in self.cart:
      del self.cart[product_id]
    # update the session
    self.session.modified = True

    if self.request.user.is_authenticated:

      current_user = Profile.objects.filter(user__id = self.request.user.id)
      # convert the single quteion to duble quteion
      carty =str(self.cart)
      carty=carty.replace("\'","\"")
      current_user.update(cart = str(carty))



  def total_price(self):
    # get the products ids from cart
    products_ids = self.cart.keys()
    # useing the ids to lookeup products in the database
    products = Product.objects.filter(id__in=products_ids)
    quantitys = self.cart
    total = 0
    for key,value in quantitys.items():
      key = int(key)
      for product in products:
        if product.id == key:
          # make the operation to get the total
          total = total + (product.price * value)
    # return the total
    return total  
  
  def clear_cart(self):
    self.cart.clear()
    self.session.modified = True
    if self.request.user.is_authenticated:
        current_user = Profile.objects.filter(user__id=self.request.user.id)
        current_user.update(cart="{}")
    return self.cart