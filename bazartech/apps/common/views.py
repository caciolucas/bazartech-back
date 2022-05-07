from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from common.models import City
from common.serializers import CitySerializer

# Create your views here.


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filterset_fields = ["state__uf"]
    search_fields = ["name", "state__uf", "state__name"]
    permission_classes = [AllowAny]
