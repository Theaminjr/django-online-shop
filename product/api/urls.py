from django.urls import path
from product.api.views import ProductCardView,ProductDetailView,CategoryListView,CategoryProductView,ProductDiscountView,ProductCommentsView

urlpatterns = [
    path('',ProductCardView.as_view()), # all products
    path('<int:id>/',ProductDetailView.as_view()), # detail of a single product
    path('category/<int:id>/',CategoryProductView.as_view()),# products inside a category and its subcategories
    path('categories/',CategoryListView.as_view()),# return categories without parent
    path('categories/<int:id>/',CategoryListView.as_view()),# return all the subcategories for a category
    path('discount/',ProductDiscountView.as_view()),# products with discount
    path('<int:id>/comments/',ProductCommentsView.as_view())#get comments for a product or create new ones
]
