from django.contrib.gis import admin
from .models import Garden, GardenSpaces, Planting

# Register your models here.

admin.site.register(Garden, admin.GeoModelAdmin)
admin.site.register(GardenSpaces, admin.GeoModelAdmin)
admin.site.register(Planting, admin.GeoModelAdmin)
