import re
from typing import List, Optional
from .models import WeatherData


class UKMetOfficeParser:

    MONTH_MAPPING = {
        "jan": "january",
        "feb": "february",
        "mar": "march",
        "apr": "april",
        "may": "may",
        "jun": "june",
        "jul": "july",
        "aug": "august",
        "sep": "september",
        "oct": "october",
        "nov": "november",
        "dec": "december",
    }

    SEASON_MAPPING = {
        "win": "winter",
        "spr": "spring",
        "sum": "summer",
        "aut": "autumn",
    }

    @classmethod
    def parse_file(cls, file_path: str) -> List[WeatherData]:

        with open(file_path, "r") as file:
            content = file.read()
        return cls.parse_content(content)

    @classmethod
    def parse_content(cls, content: str) -> List[WeatherData]:

        lines = content.strip().split("\n")

        if not lines:
            raise ValueError("Empty content provided")

        header_line = lines[0].strip()
        columns = re.split(r"\s+", header_line)

        if "year" not in columns:
            raise ValueError("Invalid format: 'year' column not found")

        weather_records = []

        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue

            try:
                record = cls._parse_line(line, columns)
                if record:
                    weather_records.append(record)
            except Exception as e:
                print(f"Warning: Failed to parse line '{line}': {e}")
                continue

        return weather_records

    @classmethod
    def _parse_line(cls, line: str, columns: List[str]) -> Optional[WeatherData]:

        values = re.split(r"\s+", line.strip())

        if len(values) != len(columns):
            raise ValueError(
                f"Column count mismatch: expected {len(columns)}, got {len(values)}"
            )

        data_dict = dict(zip(columns, values))

        try:
            year = int(data_dict["year"])
        except (ValueError, KeyError):
            raise ValueError("Invalid year value")

        weather_data = WeatherData(year=year)

        for col, field in cls.MONTH_MAPPING.items():
            if col in data_dict:
                value = cls._parse_float_value(data_dict[col])
                setattr(weather_data, field, value)

        for col, field in cls.SEASON_MAPPING.items():
            if col in data_dict:
                value = cls._parse_float_value(data_dict[col])
                setattr(weather_data, field, value)

        if "ann" in data_dict:
            weather_data.annual = cls._parse_float_value(data_dict["ann"])

        return weather_data

    @staticmethod
    def _parse_float_value(value: str) -> Optional[float]:

        if not value or value.strip() in ["---", "N/A", ""]:
            return None

        try:
            return float(value.strip())
        except ValueError:
            return None
