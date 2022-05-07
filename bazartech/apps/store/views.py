from store.models import Product
from store.permissions import OwnProductPermission
from store.serializers import ProductSerializer

from rest_framework import viewsets

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [OwnProductPermission]
