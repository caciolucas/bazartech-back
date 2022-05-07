from rest_framework import serializers

from django.db import transaction

from authentication.models import User
from common.models import Address, City
from common.serializers import AddressSerializer


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    permissions_display = serializers.ListField(source="get_all_permissions", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = User
        fields = "__all__"

    @transaction.atomic()
    def update(self, instance: User, validated_data):
        address_new_data = validated_data.pop("address")
        address_old_data = instance.address
        address_new_data["state"] = address_new_data["city"]["state"]["name"]
        address_new_data["city"] = address_new_data["city"]["name"]
        new_address = AddressSerializer(instance=address_old_data, data=address_new_data)
        if new_address.is_valid():
            new_address.save()
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    @transaction.atomic()
    def create(self, validated_data):
        address = validated_data.pop("address")
        password = validated_data.pop("password")
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
        user = User.objects.create(**validated_data, address=address_obj)
        user.set_password(password)
        user.save()
        return user
