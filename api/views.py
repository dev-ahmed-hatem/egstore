from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_product(request, *args, **kwargs):
    products = Product.objects.all()
    serializer = ProductSerializer(Product.objects.all(), many=True)
    data = {}
    # serializer.is_valid(raise_exception=True)
    # print(serializer.data)
    # if serializer.is_valid():
    #     data = serializer.data
    # if model_data:
    #     data = ProductSerializer(model_data).data
    return Response(serializer.data)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'user-list': reverse('user-list', request=request, format=format),
        'product-list': reverse('product-list', request=request, format=format),
        'category-list': reverse('category-list', request=request, format=format),
        'sale-list': reverse('sale-list', request=request, format=format),
    })


class UserList(ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetail(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SaleList(ListAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class SaleDetail(RetrieveAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer