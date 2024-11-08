from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from members.models import Profile

# Register your models here.
admin.site.site_header = 'Y-A-A'
admin.site.register(Category)
admin.site.register(Contact_Us)
admin.site.register(Profile)
admin.site.register(Product)


# mix the profile informaiton and user information
class ProfileInline(admin.StackedInline):
  model = Profile

# extends the User model
class UserAdmin(admin.ModelAdmin):
  model = User
  field = ['username','first_name','last_name','email']
  inlines =[ProfileInline]



# unregister the old way
admin.site.unregister(User)

# re-register the new way
admin.site.register(User,UserAdmin)


