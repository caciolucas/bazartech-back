from store.models import Product, ProductImage, Tag

from rest_framework import serializers

from authentication.serializers import UserSerializer
from django.db import transaction


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    tags_display = serializers.SerializerMethodField()
    owner_display = serializers.SerializerMethodField()
    images_display = serializers.SerializerMethodField()
    tags = serializers.ListField(write_only=True, allow_empty=True, child=serializers.CharField())
    pictures = serializers.ListField(
        write_only=True, allow_empty=True, child=serializers.DictField(child=serializers.CharField())
    )

    class Meta:
        model = Product
        fields = "__all__"

    def get_tags_display(self, object: Product):
        return object.tags.all().values_list("name", flat=True)

    def get_owner_display(self, object: Product):
        return UserSerializer(object.owner).data

    def get_images_display(self, object: Product):
        return ProductImageSerializer(object.images.all(), many=True).data

    @transaction.atomic()
    def create(self, validated_data):
        tags_names = validated_data.pop("tags")
        pictures = validated_data.pop("pictures")

        tags = []
        for tag_name in tags_names:
            tag = Tag.objects.get_or_create(name=tag_name.strip())
            tags.append(tag[0])

        product = Product.objects.create(**validated_data)
        product.tags.set(tags)

        for picture in pictures:
            ProductImage.objects.create(
                image=picture.get("image"), description=picture.get("description"), product=product
            )

        return product
