from django.contrib import admin
from .models import item,LoginData,cart, order
# Register your models here.
admin.site.register(item)
admin.site.register(cart)
admin.site.register(LoginData)
admin.site.register(order)
