from rest_framework import serializers
from product.models import Product,ProductImage,TableRow,ProductOption,Option,Category,Comment




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','image']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class TableRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableRow
        fields = ['key','value']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['name']

class ProductOptionSerializer(serializers.ModelSerializer):
    option = serializers.StringRelatedField()
    class Meta:
        model = ProductOption
        fields = ['id','option','value','available']


class ProductDetailsSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()
    images = ProductImageSerializer(many=True,read_only=True)
    tablerows = TableRowSerializer(many=True,read_only=True)
    options = ProductOptionSerializer(many=True,read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        depth = 1

    def get_discount(self,obj):
        return obj.has_discount().percentage if obj.has_discount() else None

class ProductCardSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id', 'thumbnail','name', 'price','discount')

    def get_discount(self,obj):
        return obj.has_discount().percentage if obj.has_discount() else None
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1
