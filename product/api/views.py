from rest_framework.views import APIView
from rest_framework.response import Response
from core.api.auth import login_required
from product.api.serializers import ProductCardSerializer,ProductDetailsSerializer,CategorySerializer,CommentSerializer
from product.models import Product,Category,Discount,Comment
from django.core.paginator import Paginator
import itertools

#returns all products with pagination
class ProductCardView(APIView):

    def get(self,request):
        page_num = request.GET.get('page',1)
        products = Product.objects.all().order_by('date')
        p = Paginator(products,8)
        page = p.page(page_num)
        serializer = ProductCardSerializer(page.object_list,many=True)
        return Response({"products":serializer.data,"page_num":p.num_pages},status=200)

# single product details
class ProductDetailView(APIView):

    def get(self,request,id):
        product = Product.objects.get(id=id)
        serializer = ProductDetailsSerializer(product)
        return Response(serializer.data,status=200)


class ProductCommentsView(APIView):
    #get comments for a specific product
    def get(self,request,id):
        try:
           product = Product.objects.get(id=id)
        except:
            return Response(status=404)
        comments = Comment.objects.filter(product=product,approved =True)
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data,status=200)
    
    #post comment for a specific product
    @login_required
    def post(self,request,id):
        try:
           product = Product.objects.get(id=id)
        except:
            return Response(status=404)
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.jwt ,product=product)
            return Response(status=201)
        return Response(status=404)


#return categoris without parent if id not provided/ return all th subcategories for the category which its id is provided
class CategoryListView(APIView):

    def get(self,request,id=None):
        if id:
            try:
               category = Category.objects.get(id=id)
            except:
                Response(status=404)
            categories = category.subs.all()
        else:
           categories = Category.objects.filter(parent=None)
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data,status=200)


#return products inside a category and its sub categories with pagination
class CategoryProductView(APIView):

    def get(self,request,id=None):
        try:
          category = Category.objects.get(id=id)
        except:
            Response(status=404)
        categories = category.all_subs()
        categories.append(category)
        products = [category.products.all() for category in categories if category.products.all()] #list of querysets
        products = list(itertools.chain(*products)) # unpack querysets inside a list
        page_num = request.GET.get('page',1)
        p = Paginator(products,8)
        page = p.page(page_num)
        serializer = ProductCardSerializer(page.object_list,many=True)
        return Response({"products":serializer.data,"page_num":p.num_pages},status=200)

# returns products with discounts
class ProductDiscountView(APIView):

    def get(self,request):
        page_num = request.GET.get('page',1)
        discounts = Discount.active()
        products = [ discount.category.products.all() for discount in discounts if discount.category ]
        products = list(itertools.chain(*products)) + [discount.product for discount in discounts if discount.product]
        p = Paginator(products,8)
        page = p.page(page_num)
        serializer = ProductCardSerializer(page.object_list,many=True)
        return Response({"products":serializer.data,"page_num":p.num_pages},status=200)