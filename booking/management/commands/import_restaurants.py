from django.core.management.base import BaseCommand
from booking.models import Restaurant
import csv

class Command(BaseCommand):
    help = 'Load a list of restaurants from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The path to the CSV file to import.')

    def handle(self, *args, **options):
        path = options['csv_file_path']
        with open(path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            reader.fieldnames = [name.encode('utf-8').decode('utf-8-sig').strip() for name in reader.fieldnames]
            for row in reader:
                Restaurant.objects.create(
                    code=row['code'],
                    name=row['nom_restaurant'],
                    address=row['adresse'],
                    city=row['ville'],
                    tt=row['tt'],
                    type=row['type'],
                    capacity=0,  # Default capacity value
                    description="No description available"  # Default description
                )
            self.stdout.write(self.style.SUCCESS('Successfully loaded restaurants into the database'))
