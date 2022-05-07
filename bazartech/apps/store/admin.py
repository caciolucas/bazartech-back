from store.models import Product, ProductImage, Tag

from django.contrib import admin

# Register your models here.

admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(ProductImage)
