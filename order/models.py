from django.db import models
from core.models import User,Address
from product.models import Product,ProductOption
# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = [('PENDING','PENDING'),('DELIVERED',"DELIVERED"),("CANCELED","CENCELED")]
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    address = models.ForeignKey(Address,on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='PENDING')

    @property
    def price(self):
        price = 0
        for item in OrderItem.objects.filter(order=self):
            price += item.price
        return price
    
    @property
    def discount(self):
        discount = 0
        for item in OrderItem.objects.filter(order=self):
            discount += item.discount if item.discount else 0
        return discount
    
    @property
    def total(self):
        return self.price - self.discount
        
        
    def __str__(self):
        return f'{self.date}'





class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT,)
    product_option = models.ForeignKey(ProductOption,on_delete=models.PROTECT,null=True,blank=True)
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='orderitems')
    price = models.PositiveIntegerField(null=True)
    discount = models.PositiveIntegerField(null=True)
    
    
    def save(self, *args, **kwargs):
       self.price = self.product.price * self.count
       discount = self.product.has_discount()
       self.discount = discount.decimal * self.price if discount else 0
       super(OrderItem, self).save(*args, **kwargs)
