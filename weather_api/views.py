from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Max, Min
from django.shortcuts import get_object_or_404
from .models import WeatherData
from .pagination import WeatherPagination
from .serializers import WeatherDataSerializer, WeatherDataSummarySerializer


class WeatherDataViewSet(viewsets.ModelViewSet):

    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    pagination_class = WeatherPagination

    def get_queryset(self):
        queryset = WeatherData.objects.all().order_by("-year")
        year = self.request.query_params.get("year", None)
        year_from = self.request.query_params.get("year_from", None)
        year_to = self.request.query_params.get("year_to", None)
        page = self.request.query_params.get("page", None)

        if year is not None:
            queryset = queryset.filter(year=year)
        if year_from is not None:
            queryset = queryset.filter(year__gte=year_from)
        if year_to is not None:
            queryset = queryset.filter(year__lte=year_to)

        if not queryset.exists():
            return Response(
                {"error": "No data available"}, status=status.HTTP_404_NOT_FOUND
            )

        return queryset

    @action(detail=False, methods=["get"])
    def summary(self, request):

        self.serializer_class = WeatherDataSummarySerializer
        return super().list(request)

    @action(detail=False, methods=["get"])
    def statistics(self, request):

        queryset = self.get_queryset()

        if not queryset.exists():
            return Response(
                {"error": "No data available"}, status=status.HTTP_404_NOT_FOUND
            )

        annual_stats = queryset.aggregate(
            avg_temperature=Avg("annual"),
            max_temperature=Max("annual"),
            min_temperature=Min("annual"),
        )

        seasonal_stats = {
            "winter": queryset.aggregate(
                avg=Avg("winter"), max=Max("winter"), min=Min("winter")
            ),
            "spring": queryset.aggregate(
                avg=Avg("spring"), max=Max("spring"), min=Min("spring")
            ),
            "summer": queryset.aggregate(
                avg=Avg("summer"), max=Max("summer"), min=Min("summer")
            ),
            "autumn": queryset.aggregate(
                avg=Avg("autumn"), max=Max("autumn"), min=Min("autumn")
            ),
        }

        hottest_year = queryset.order_by("-annual").first()
        coldest_year = queryset.order_by("annual").first()

        return Response(
            {
                "total_records": queryset.count(),
                "year_range": {
                    "from": queryset.order_by("year").first().year,
                    "to": queryset.order_by("-year").first().year,
                },
                "annual_statistics": annual_stats,
                "seasonal_statistics": seasonal_stats,
                "extreme_years": {
                    "hottest": (
                        {"year": hottest_year.year, "temperature": hottest_year.annual}
                        if hottest_year
                        else None
                    ),
                    "coldest": (
                        {"year": coldest_year.year, "temperature": coldest_year.annual}
                        if coldest_year
                        else None
                    ),
                },
            }
        )

    @action(detail=True, methods=["get"])
    def monthly_breakdown(self, request, pk=None):

        weather_data = self.get_object()
        monthly_data = weather_data.monthly_data

        valid_months = {k: v for k, v in monthly_data.items() if v is not None}
        sorted_months = sorted(valid_months.items(), key=lambda x: x[1])

        return Response(
            {
                "year": weather_data.year,
                "monthly_temperatures": monthly_data,
                "seasonal_temperatures": weather_data.seasonal_data,
                "annual_average": weather_data.annual,
                "temperature_range": {
                    "coldest_month": {
                        "month": sorted_months[0][0] if sorted_months else None,
                        "temperature": sorted_months[0][1] if sorted_months else None,
                    },
                    "warmest_month": {
                        "month": sorted_months[-1][0] if sorted_months else None,
                        "temperature": sorted_months[-1][1] if sorted_months else None,
                    },
                },
            }
        )
