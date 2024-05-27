from django.urls import path
from .views import *
from .serializers import *

urlpatterns = [
    path("", api_root, name="root"),
    path("user-list/", UserList.as_view(), name="user-list"),
    path("user/<int:pk>", UserDetail.as_view(), name="user"),
    path("product-list/", ProductList.as_view(), name="product-list"),
    path("product/<int:pk>", ProductDetail.as_view(), name="product"),
    path("category-list/", CategoryList.as_view(), name="category-list"),
    path("category/<int:pk>/", CategoryDetail.as_view(), name="category"),
    path("sale-list/", SaleList.as_view(), name="sale-list"),
    path("sale/<int:pk>/", SaleDetail.as_view(), name="sale"),
]


