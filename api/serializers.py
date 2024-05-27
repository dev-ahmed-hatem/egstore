from rest_framework import serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import *
from rest_framework import permissions


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "first_name", "last_name", "phone_number", "picture", "is_admin"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    sale = SaleSerializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "title", "price", "description", "images", "category", "sale"]
        # fields = '__all__'

    title = serializers.CharField(required=False)
    price = serializers.FloatField(required=False)
    description = serializers.CharField(required=False)

    def get_images(self, obj):
        request = self.context.get("request")
        product_images = obj.images.all()
        return  [request.build_absolute_uri(image.image.url) for image in product_images]
