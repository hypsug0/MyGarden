"""Models"""

from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from plantinfos.models import (
    HardinessZone,
    OperationsList,
    PlantOperations,
    Plants,
)

# Create your models here.


class Garden(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=250)
    geom = models.MultiPolygonField(
        verbose_name=_("Geom"), blank=True, null=True, srid=4326
    )
    geo_zone = models.ForeignKey(
        HardinessZone,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Geographic zone"),
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("garden")
        verbose_name_plural = _("gardens")

    def __str__(self):
        return self.name


class GardenSpaces(models.Model):
    """_summary_

    :param models: _description_
    :type models: _type_
    :return: _description_
    :rtype: _type_
    """

    name = models.CharField(verbose_name=_("Name"), max_length=250)
    geom = models.MultiPolygonField(
        verbose_name=_("Geom"), blank=True, null=True
    )
    garden = models.ForeignKey(
        Garden, on_delete=models.CASCADE, verbose_name=_("Garden")
    )

    class Meta:
        verbose_name = _("garden space")
        verbose_name_plural = _("garden spaces")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class Planting(models.Model):
    plant = models.ForeignKey(
        Plants, on_delete=models.CASCADE, verbose_name=_("Plant")
    )
    geom = models.GeometryField(
        blank=True, null=True, verbose_name=_("Location"), srid=4326
    )

    class Meta:
        verbose_name = _("garden space")
        verbose_name_plural = _("garden spaces")

    def __str__(self):
        name = (
            self.plant.common_name
            if self.plant.common_name
            else (self.plant.sci_name if self.plant.sci_name else "???")
        )
        return f"{name} ({self.date})"


class Operations(models.Model):
    planting = models.ForeignKey(
        Planting, on_delete=models.CASCADE, verbose_name=_("Plant")
    )
    date = models.DateField(_("Date"), blank=True, null=True)
    operation = models.ManyToManyField(OperationsList)

    class Meta:
        verbose_name = _("garden space")
        verbose_name_plural = _("garden spaces")

    def __str__(self):
        name = (
            self.plant.common_name
            if self.plant.common_name
            else (self.plant.sci_name if self.plant.sci_name else "???")
        )
        return f"{name} ({self.date})"
