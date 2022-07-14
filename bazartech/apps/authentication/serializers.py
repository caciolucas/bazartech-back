from rest_framework import serializers

from django.db import transaction

from authentication.models import User
from common.models import Address, City
from common.serializers import AddressSerializer


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    permissions_display = serializers.ListField(source="get_all_permissions", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    favorite_products_display = serializers.SerializerMethodField()
    favorite_products = serializers.ListField(
        write_only=True, allow_empty=True, child=serializers.IntegerField(), required=False
    )
    username = serializers.CharField(required=False)
    optional_fields = ["address", "favorite_products", "username"]

    class Meta:
        model = User
        fields = "__all__"

    def get_favorite_products_display(self, object: User):
        return object.favorite_products.all().values_list("id", flat=True)

    @transaction.atomic()
    def update(self, instance: User, validated_data):
        address_new_data = validated_data.pop("address", None)
        if address_new_data and instance.address:
            address_old_data = instance.address
            address_new_data["state"] = address_new_data["city"]["state"]["name"]
            address_new_data["city"] = address_new_data["city"]["name"]
            new_address = AddressSerializer(instance=address_old_data, data=address_new_data)
            if new_address.is_valid():
                new_address.save()
        if address_new_data and not instance.address:
            address_obj = Address.objects.create(
                zip_code=address_new_data["zip_code"],
                street=address_new_data["street"],
                number=address_new_data["number"],
                district=address_new_data["district"],
                city=City.objects.get(
                    name__iexact=address_new_data["city"]["name"],
                    state__name__iexact=address_new_data["city"]["state"]["name"],
                ),
            )
            instance.address = address_obj
            instance.save()
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        favorite_products = validated_data.pop("favorite_products", None)
        if favorite_products:
            instance.favorite_products.set(favorite_products)
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    @transaction.atomic()
    def create(self, validated_data):
        username = validated_data.pop("username", None)

        if username == None:
            username = validated_data.pop("email")

        if validated_data.get("address"):

            password = validated_data.pop("password")
            address = validated_data.pop("address")
            address_obj = Address.objects.create(
                zip_code=address["zip_code"],
                street=address["street"],
                number=address["number"],
                district=address["district"],
                city=City.objects.get(
                    name__iexact=address["city"]["name"],
                    state__name__iexact=address["city"]["state"]["name"],
                ),
            )
            user = User.objects.create(**validated_data, address=address_obj, username=username)
            user.set_password(password)
            user.save()
            return user
        else:
            password = validated_data.pop("password")
            user = User.objects.create(**validated_data, username=username)
            user.set_password(password)
            user.save()
            return user
