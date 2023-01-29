from django.contrib import admin

from .models import (
    Conditions,
    HardinessZone,
    OperationsList,
    PlantOperations,
    Plants,
)

# Register your models here.

admin.site.register(HardinessZone, admin.ModelAdmin)
admin.site.register(OperationsList, admin.ModelAdmin)
admin.site.register(Plants, admin.ModelAdmin)
admin.site.register(PlantOperations, admin.ModelAdmin)
admin.site.register(Conditions, admin.ModelAdmin)
