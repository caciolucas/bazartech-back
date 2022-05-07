from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup

from authentication.models import Group, Permission, User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["profile_picture"]


admin.site.register(Permission)
admin.site.register(Group)
admin.site.unregister(DjangoGroup)
