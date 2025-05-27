from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from weather_api.parsers import UKMetOfficeParser
from weather_api.models import WeatherData
import os


class Command(BaseCommand):
    help = "Import weather data from UK MetOffice format file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the weather data file")
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Replace existing data for duplicate years",
        )
        parser.add_argument(
            "--clear", action="store_true", help="Clear all existing data before import"
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]

        if not os.path.exists(file_path):
            raise CommandError(f'File "{file_path}" does not exist')

        try:
            self.stdout.write(f"Parsing file: {file_path}")
            weather_records = UKMetOfficeParser.parse_file(file_path)

            if not weather_records:
                self.stdout.write(
                    self.style.WARNING("No valid weather records found in file")
                )
                return

            self.stdout.write(f"Found {len(weather_records)} weather records")

            with transaction.atomic():
                if options["clear"]:
                    self.stdout.write("Clearing existing weather data...")
                    WeatherData.objects.all().delete()

                created_count = 0
                updated_count = 0
                skipped_count = 0

                for record in weather_records:
                    try:
                        existing = WeatherData.objects.filter(year=record.year).first()

                        if existing:
                            if options["replace"]:
                                for field in [
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
                                ]:
                                    setattr(existing, field, getattr(record, field))
                                existing.save()
                                updated_count += 1
                            else:
                                skipped_count += 1
                                continue
                        else:
                            record.save()
                            created_count += 1

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Error processing year {record.year}: {e}"
                            )
                        )
                        continue

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Import completed:\n"
                        f"  Created: {created_count} records\n"
                        f"  Updated: {updated_count} records\n"
                        f"  Skipped: {skipped_count} records"
                    )
                )

        except Exception as e:
            raise CommandError(f"Error importing data: {e}")
