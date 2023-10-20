from django.contrib import admin
from order.models import Order,OrderItem
# Register your models here.



class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['date','price','discount','total']
    inlines = [OrderItemInline]
    
admin.site.register(Order,OrderAdmin)