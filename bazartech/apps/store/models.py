from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AutoTimestamps

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


class Product(AutoTimestamps):
    HIDDEN = 0
    AVAILABLE = 1
    SELLED = 2

    STATUS_CHOICES = (
        (HIDDEN, _("Hidden")),
        (AVAILABLE, _("Available")),
        (SELLED, _("Selled")),
    )
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"))
    tags = models.ManyToManyField("store.Tag", related_name="products", verbose_name=_("Tags"))
    price = models.DecimalField(_("Price"), max_digits=7, decimal_places=2)
    status = models.IntegerField(_("Status"), choices=STATUS_CHOICES)
    owner = models.ForeignKey("authentication.User", models.CASCADE, related_name="products", verbose_name=_("Owner"))
    favorite = models.ManyToManyField(
        "authentication.User", related_name="favorite_products", verbose_name=_("Favorite")
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self) -> str:
        return f"{self.name}"


class ProductImage(models.Model):
    image = models.TextField(_("Image URL"))
    description = models.TextField(_("Description"))
    product = models.ForeignKey(
        "store.Product", on_delete=models.CASCADE, related_name="images", verbose_name=_("Product")
    )

    class Meta:
        verbose_name = _("Product's image")
        verbose_name_plural = _("Product's images")

    def __str__(self) -> str:
        return f"{self.product.name} - {self.description}"
