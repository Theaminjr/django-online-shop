from django.db import models
from django_cleanup import cleanup
from core.models import User
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.html import mark_safe


@cleanup.select
class Category(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,related_name='subs')

    def all_subs(self): # return subcategories with infinite depth
        sub_categories = []
        for category in self.subs.all():
            sub_categories.append(category)
            sub_categories += category.all_subs()
        return sub_categories

    def __str__(self):
        return self.name
    
@cleanup.select
class Product(models.Model):
    code = models.PositiveBigIntegerField()
    thumbnail = models.ImageField()
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    available = models.BooleanField(default=True)
    recommended = models.BooleanField(default=False)
    sold = models.PositiveBigIntegerField(default=0)
    view = models.PositiveBigIntegerField(default=0)

    date = models.DateField(auto_now=True)

    categories = models.ManyToManyField(Category,related_name='products')

    def has_discount(self):
        discounts = Discount.active()
        categories_dis = [discount for discount in discounts if discount.category in self.categories.all()] # list of discounts that share their category with product categories
        products_dis = [discount for discount in discounts if discount.product == self] # list of discounts that have the same product as product
        return products_dis[0] if products_dis else categories_dis[0] if categories_dis else None # product discount has higher priority than category discounts
    
    @property
    def admin_thumbnail(self):
       return mark_safe('<img style="height:125px;" src="%s" />' % self.thumbnail.url)

    def __str__(self):
        return self.name
    
        
    

class TableRow(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='tablerows')

    def __str__(self):
        return f"{self.product.name}-{self.id}"


@cleanup.select
class ProductImage(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')

    def save(self, *args, **kwargs):
        self.name = f"{self.product.name}-{self.id}" 
        super(ProductImage,self).save(*args, **kwargs)


class Option(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class ProductOption(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='options')
    option = models.ForeignKey(Option,on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.option.name}::{self.value}"


class Discount(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True,related_name='discount')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name='discount')
    start_date = models.DateField()
    end_date = models.DateField()
    percentage = models.PositiveIntegerField(validators=[MaxValueValidator(100),MinValueValidator(1)])
    
    @classmethod
    def active(self):
        today = datetime.datetime.now()
        return Discount.objects.filter(end_date__gte = today)
        
    
    @property
    def decimal(self):
        return  self.percentage/100
    
    def __str__(self):
        return f"{self.start_date}"
    

class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()