from store.models import Product, ProductImage

from rest_framework import serializers

from authentication.serializers import UserSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    tags_display = serializers.SerializerMethodField()
    owner_display = serializers.SerializerMethodField()
    images_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_tags_display(self, object: Product):
        return object.tags.all().values_list("name", flat=True)

    def get_owner_display(self, object: Product):
        return UserSerializer(object.owner).data

    def get_images_display(self, object: Product):
        return ProductImageSerializer(object.images.all(), many=True).data
