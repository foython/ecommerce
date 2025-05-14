import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from .models import MainCategory, Product, ProductImage, SizeandQuantity
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.paginator import Paginator
import json
from cart.models import Cart
import random
import string
from datetime import datetime, timedelta


# Create your views here.

class IndexView(View):
    def get(self, request):               
        allproduct = Product.objects.all().order_by('-created_at')        
        related_sizeq = SizeandQuantity.objects.all()
        context = {'products': allproduct, 'product_size': related_sizeq,}
        cooki = request.COOKIES.get('key')

        if not cooki:
            cookie_value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
            response = render(request, 'home.html', context)
            response.set_cookie('key', cookie_value, expires=datetime.utcnow()+timedelta(days=15))
            return response
        else:
            return render(request, 'home.html', context)


class DetailsView(View):
    def get(self, request, id):        
        item = Product.objects.get(pk=id) 
        sizeq = SizeandQuantity.objects.filter(product__id=id)       
        images = item.multi_images.all()              
        r_cart = Cart.objects.filter(session=request.COOKIES.get('key')).values('product_id')   
        related = Product.objects.filter(main_category__name=item.main_category).exclude(id__in=r_cart).exclude(id=id)
        related_sizeq = SizeandQuantity.objects.all()
        c_url =  request.build_absolute_uri()
        print(c_url)

        con = False

        for i in r_cart:
            if i['product_id'] == item.id:
                con = True
                break
            else:
                con = False

        context = {'item': item, 'images': images, 'sizeq': sizeq, 'related': related, 'product_size': related_sizeq, 'in_cart':con}
        cooki = request.COOKIES.get('key')
        if not cooki:
            cookie_value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
            response = render(request, 'product-details.html', context)
            response.set_cookie('key', cookie_value, expires=datetime.utcnow()+timedelta(days=15))
            return response
        else:
            return render(request, 'product-details.html', context)


@login_required()
def send_sub(request):
    take = json.loads(request.body)
    main_cat = take['main_id']
    sub_category = {}
    if main_cat:
        sub_cats = MainCategory.objects.get(pk=main_cat).sub_cat.all()
        sub_category = {pp.name: pp.id for pp in sub_cats}
    return JsonResponse(data=sub_category, safe=False)


class ShopView(View):
    def get(self, request, name=None):
        if name:
            product_list = Product.objects.filter(sub_category__name=self.kwargs['name']).order_by('-id')
            if not product_list:
                product_list = Product.objects.filter(main_category__name=self.kwargs['name']).order_by('-id')
        else:
            product_list = Product.objects.all().order_by('-id')
               
        p = Paginator(product_list, 9)         
        page = request.GET.get('page')        
        allproduct = p.get_page(page) 
        product_size = SizeandQuantity.objects.all()
        context = { 'products': allproduct, 'p':p, 'product_size': product_size}
        cooki = request.COOKIES.get('key')
        if not cooki:
            cookie_value = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
            response = render(request, 'shop.html', context)
            response.set_cookie('key', cookie_value, expires=datetime.utcnow()+timedelta(days=15))
            return response
        else:        
            return render(request, 'shop.html', context)
       
        

         
                     
        

class FilterShopView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(sub_category__name=self.kwargs['name'])


'''def get_context_data(self):
    image_list = ProductImage.objects.all()
    context = {'image_list': image_list}
    return context'''


# class ProductAPI(APIView):

#     def get(self, request, id=None, format=None):
#         pk = id
#         if pk is not None:
#             product = Product.objects.get(pk=pk)
#             serializer = ProductSerializer(product)
#             return Response(serializer.data)

#         product = Product.objects.all()
#         serializer = ProductSerializer(product, many=True)
#         return Response(serializer.data)



