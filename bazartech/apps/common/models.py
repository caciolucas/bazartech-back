from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class AutoTimestamps(models.Model):
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        abstract = True


class City(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    state = models.ForeignKey("State", on_delete=models.CASCADE, verbose_name=_("State"))
    ibge_code = models.CharField(_("IBGE code"), max_length=255)

    def __str__(self):
        return f"{self.name} ({self.state.uf})"

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        ordering = ["state", "name"]


class State(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    uf = models.CharField(_("UF"), max_length=2)
    uf_code = models.CharField(_("UF Code"), max_length=255)

    def __str__(self):
        return f"{self.name} - {self.uf}"

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")


class Address(AutoTimestamps):
    zip_code = models.CharField(_("Zip code"), max_length=12)
    street = models.CharField(_("Street"), max_length=255)
    number = models.CharField(_("Number"), max_length=255)
    district = models.CharField(_("District"), max_length=255)
    city = models.ForeignKey("City", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.street}, {self.number} -  {self.district}, {self.city}"

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
