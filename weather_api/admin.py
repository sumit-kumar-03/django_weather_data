from django.contrib import admin
from .models import WeatherData


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = [
        "year",
        "annual",
        "winter",
        "spring",
        "summer",
        "autumn",
        "created_at",
    ]
    list_filter = ["year"]
    ordering = ["-year"]
    search_fields = ["year"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("year", "annual")}),
        (
            "Monthly Data",
            {
                "fields": (
                    ("january", "february", "march"),
                    ("april", "may", "june"),
                    ("july", "august", "september"),
                    ("october", "november", "december"),
                )
            },
        ),
        ("Seasonal Data", {"fields": (("winter", "spring"), ("summer", "autumn"))}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
