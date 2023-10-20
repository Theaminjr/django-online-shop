from django.urls import path
from order.api.views import OrderView
urlpatterns = [
    path("",OrderView.as_view()),
]
