from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from login.models import Hotel
import csv
import os
import math

class Command(BaseCommand):
    help = 'Import hotels data from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('hotels_in_nepali_city.csv', type=str, help='D:\3rd Year\FYP\Nepal AdvenTour\Development\Main Nepal Adventour\Nepal-AdvenTOUR-MAIN\Model\hotels_in_nepali_city.csv')

    def handle(self, *args, **options):
        csv_filename = options['csv_filename']
        try:
            with open(csv_filename, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        hotel, created = Hotel.objects.update_or_create(
                            name=row['name'],
                            defaults={
                                'type_of_hotel': row.get('type_of_hotel', 'Default Type'),
                                'address': row['address'],
                                'city': row['city'],
                                'contact': row.get('contact', ''),
                                'description': row.get('description', ''),
                                'latitude': float(row['latitude']),
                                'longitude': float(row['longitude']),
                                # 'picture': Handle image field if necessary
                            }
                        )
                        self.stdout.write(self.style.SUCCESS(f'Successfully imported hotel "{hotel.name}"'))
                    except IntegrityError as e:
                        self.stdout.write(self.style.WARNING(f'Could not import hotel "{row["name"]}": {e}'))
                    except ValueError as e:
                        self.stdout.write(self.style.WARNING(f'Invalid data for hotel "{row["name"]}": {e}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{csv_filename}" not found.'))
