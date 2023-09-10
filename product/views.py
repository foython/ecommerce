import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from .models import MainCategory, Product, ProductImage
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from cart.models import Cart


# Create your views here.

class IndexView(View):
    def get(self, request):
        allproduct = Product.objects.all().order_by('-id')
        
        context = {'product': allproduct}
        return render(request, 'home.html', context)


class DetailsView(View):
    def get(self, request, id):
        item = Product.objects.get(pk=id)
        
        images = item.multi_images.all()              
        r_cart = Cart.objects.filter(session=request.session.session_key).values('product_id')   
        related = Product.objects.filter(main_category__name=item.main_category).exclude(id__in=r_cart).exclude(id=id)
        print(r_cart)
        con = False
        for i in r_cart:
            if i['product_id'] == item.id:
                con = True
                break
            else:
                con = False

        context = {'item': item, 'images': images, 'related': related, 'in_cart':con}
        
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


class ShopView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    

    def get_queryset(self):
        
        # cart_total = cart
        
        cart = Cart.objects.filter(session=self.request.session.session_key).values()
        product_in_cart = []
        for item in cart:
            product_in_cart.append(item['product_id'])

        queryset ={'all_products': Product.objects.all(),
                   
                   'cart_items': product_in_cart,
                   
        }
        
        return queryset


class FilterShopView(ListView):
    model = Product
    template_name = 'shop.html'

    def get_queryset(self):
        return Product.objects.filter(sub_category__name=self.kwargs['name'])


'''def get_context_data(self):
    image_list = ProductImage.objects.all()
    context = {'image_list': image_list}
    return context'''


class ProductAPI(APIView):

    def get(self, request, id=None, format=None):
        pk = id
        if pk is not None:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)

        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)


def test(request):
    return HttpResponse('hello world')


