from django.contrib import admin
from . import models

admin.site.register(models.Forecast)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "state",
        "status",
    ]


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "timestamp",
        "expiry_pick_up_time",
        "status",
    ]


@admin.register(models.RunTrigger)
class RunTriggerAdmin(admin.ModelAdmin):
    list_display = (
        "time_run",
        "status",
        "error",
    )


@admin.register(models.JobTrigger)
class CreateTriggerAdmin(admin.ModelAdmin):
    list_display = (
        "trigger",
        "unique_id",
        "type",
        "finished_time",
    )
