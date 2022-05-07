from rest_framework import serializers

from common.models import Address, City


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="city.name")
    state = serializers.CharField(source="city.state.name")

    class Meta:
        model = Address
        fields = "__all__"

    def update(self, instance, validated_data):
        city_data = validated_data.pop("city")
        instance.city = City.objects.get(
            name__iexact=city_data["name"],
            state__name__iexact=city_data["state"]["name"],
        )
        return super().update(instance, validated_data)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
