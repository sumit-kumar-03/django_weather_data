from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class WeatherData(models.Model):

    year = models.IntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(2100)]
    )

    january = models.FloatField(null=True, blank=True)
    february = models.FloatField(null=True, blank=True)
    march = models.FloatField(null=True, blank=True)
    april = models.FloatField(null=True, blank=True)
    may = models.FloatField(null=True, blank=True)
    june = models.FloatField(null=True, blank=True)
    july = models.FloatField(null=True, blank=True)
    august = models.FloatField(null=True, blank=True)
    september = models.FloatField(null=True, blank=True)
    october = models.FloatField(null=True, blank=True)
    november = models.FloatField(null=True, blank=True)
    december = models.FloatField(null=True, blank=True)

    winter = models.FloatField(null=True, blank=True)
    spring = models.FloatField(null=True, blank=True)
    summer = models.FloatField(null=True, blank=True)
    autumn = models.FloatField(null=True, blank=True)

    annual = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["year"]
        unique_together = ["year"]
        verbose_name = "Weather Data"
        verbose_name_plural = "Weather Data"

    def __str__(self):
        return f"Weather Data {self.year} (Annual: {self.annual}°C)"

    @property
    def monthly_data(self):
        return {
            "january": self.january,
            "february": self.february,
            "march": self.march,
            "april": self.april,
            "may": self.may,
            "june": self.june,
            "july": self.july,
            "august": self.august,
            "september": self.september,
            "october": self.october,
            "november": self.november,
            "december": self.december,
        }

    @property
    def seasonal_data(self):
        return {
            "winter": self.winter,
            "spring": self.spring,
            "summer": self.summer,
            "autumn": self.autumn,
        }
