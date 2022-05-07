import django_filters

from authentication.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "name": ["icontains"],
        }
