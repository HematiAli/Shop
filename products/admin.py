from django.contrib import admin
from . import models


admin.site.register(models.Category)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)
