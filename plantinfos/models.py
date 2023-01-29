from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Plants(models.Model):
    sci_name = models.CharField(
        verbose_name="Scientific name", blank=True, null=True, max_length=250
    )
    common_name = models.CharField(
        verbose_name="Common name", blank=True, null=True, max_length=250
    )
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Plant")
        verbose_name_plural = _("Plants list")

    def __str__(self):
        name = (
            self.common_name
            if self.common_name
            else (self.sci_name if self.sci_name else "???")
        )
        return f"{name}"


class OperationsList(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=250)

    class Meta:
        verbose_name = _("Operation")
        verbose_name_plural = _("Operations list")

    def __str__(self):
        return self.name


class HardinessZone(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=250)
    geom = models.MultiPolygonField(
        verbose_name=_("Geom"), blank=True, null=True, srid=4326
    )

    class Meta:
        verbose_name = _("hardiness zone")
        verbose_name_plural = _("hardiness zones")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class Conditions(models.Model):
    name = models.CharField(_("Name"), max_length=250)

    class Meta:
        verbose_name = _("Condition")
        verbose_name_plural = _("Conditions")

    def __str__(self):
        return self.name


class PlantOperations(models.Model):
    plant = models.ForeignKey(Plants, on_delete=models.CASCADE)
    operation = models.ForeignKey(OperationsList, on_delete=models.CASCADE)

    start_month = models.IntegerField(_("Start month"))
    start_day = models.IntegerField(_("Start day"), blank=True, null=True)
    end_month = models.IntegerField(_("End month"))
    end_day = models.IntegerField(_("End day"), blank=True, null=True)
    geo_zone = models.ManyToManyField(HardinessZone)

    instructions = models.TextField(_("Instructions"), blank=True, null=True)
    conditions = models.ManyToManyField(Conditions, verbose_name="Conditions")

    class Meta:
        verbose_name = _("plant operation")
        verbose_name_plural = _("plant operations")

    def __str__(self):
        return f"{self.plant} - {self.operation} - {self.conditions}"
