from rest_framework import serializers
from .models import WeatherData


class WeatherDataSerializer(serializers.ModelSerializer):
    monthly_data = serializers.ReadOnlyField()
    seasonal_data = serializers.ReadOnlyField()

    class Meta:
        model = WeatherData
        fields = [
            "id",
            "year",
            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
            "winter",
            "spring",
            "summer",
            "autumn",
            "annual",
            "monthly_data",
            "seasonal_data",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class WeatherDataSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = WeatherData
        fields = ["id", "year", "annual", "winter", "spring", "summer", "autumn"]
