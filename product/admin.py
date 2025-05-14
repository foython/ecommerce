from django.contrib import admin
from .models import Product, MainCategory, SubCategory, SizeandQuantity, ProductImage
from .form import ProductForm
# Register your models here.


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


class SizeandQuantityAdmin(admin.StackedInline):
    model = SizeandQuantity
    


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, SizeandQuantityAdmin]
    #form = ProductForm
    list_display = [ 'id','name', 'main_category', 'sub_category', 'price']

    class Media:
        js = ('category.js',)

    class Meta:
        model = Product


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

# @admin.register(SizeandQuantity)
# class SizeandQuantityAdmin(admin.ModelAdmin):
#     pass

# class SizeandQuantityAdmin(admin.StackedInline):
#     model = SizeandQuantity
#     extra = 1


admin.site.register(MainCategory)
admin.site.register(SubCategory)
admin.site.register(SizeandQuantity)

