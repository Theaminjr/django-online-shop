from django.contrib import admin
from product.models import Product,ProductImage,TableRow,Category,ProductOption,Option,Discount,Comment
# Register your models here.

class TableRowInline(admin.TabularInline):
    model = TableRow

class ProductOptionInline(admin.TabularInline):
    model = ProductOption

class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['name']

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInLine,TableRowInline,ProductOptionInline]
    list_display = ['admin_thumbnail','name','price','available']
    list_filter = ['available','categories']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','product','approved']
    list_filter = ['approved']
    readonly_fields = ['user','text','product']
    

admin.site.register(Comment,CommentAdmin)
admin.site.register(Option)
admin.site.register(Discount)
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
