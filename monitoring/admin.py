from django.contrib import admin

from monitoring.models import User, Marketplace, Product, UserProduct

admin.site.register(User)
admin.site.register(Marketplace)
admin.site.register(Product)
admin.site.register(UserProduct)
# Register your models here.
