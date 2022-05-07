from itertools import chain

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin as BasicPermissionsMixin, UserManager as BaseUserManager
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Permission(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    codename = models.CharField(_("Codename"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")

    def __str__(self):
        return "%s" % self.name


class Group(models.Model):
    name = models.CharField(_("name"), max_length=150, unique=True)
    permissions = models.ManyToManyField(Permission, verbose_name=_("permissions"), blank=True)

    class Meta:
        app_label = "authentication"
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self):
        return self.name


class PermissionsMixin(BasicPermissionsMixin):

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions " "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_all_permissions(self):
        """Return a list of all permissions that this user has by itself and
        through their groups."""
        group_permissions = self.groups.values_list("permissions__codename", flat=True)
        group_permissions = [permission for permission in group_permissions if permission]
        user_permissions = self.user_permissions.values_list("codename", flat=True)
        group_permissions = [permission for permission in group_permissions if permission]
        return set(chain(group_permissions, user_permissions))


class UserManager(BaseUserManager):
    def create_user(self, name, password, username):
        if not username:
            raise ValueError("Please provide an username")
        user = self.model(name=name, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password, username, **extra_fields):
        usuario = self.create_user(name, password, username)
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)


class User(AbstractBaseUser, PermissionsMixin):
    DEFAULT_PROFILE_PICTURE_BASE64 = "QmXBdsBBD6cpXuFg9fCWrpQBhLmntHyLwh3EgvPHVP8UxL"

    name = models.CharField(_("Name"), max_length=255)
    username = models.CharField(_("User"), max_length=255, unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(_("Email"), unique=True, null=True, blank=True)
    address = models.ForeignKey(
        "common.Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Address"),
    )
    birthdate = models.DateField(_("Birthdate"), null=True, blank=True)
    gender = models.CharField(_("Gender"), max_length=1, null=True, blank=True)
    profile_picture = models.TextField(
        _("Profile picture"), null=True, blank=True, default=DEFAULT_PROFILE_PICTURE_BASE64
    )
    is_staff = models.BooleanField(
        _("Staff"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    registered_at = models.DateTimeField(_("Registered at"), auto_now_add=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    class Meta:
        app_label = "authentication"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.name}"


@receiver(post_save, sender=User)
def user_post_save(sender, instance: User, created, **kwargs):
    if not instance.profile_picture:
        instance.profile_picture = instance.DEFAULT_PROFILE_PICTURE_BASE64
        instance.save()


@receiver(post_delete, sender=User)
def user_post_delete(sender, instance: User, **kwargs):
    try:
        if instance.address:
            instance.address.delete()
    except:
        pass
