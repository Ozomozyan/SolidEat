# booking/management/commands/delete_expired_reservations.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from booking.models import Reservation

class Command(BaseCommand):
    help = 'Deletes reservations that have passed'

    def handle(self, *args, **options):
        current_datetime = timezone.now()
        expired_reservations = Reservation.objects.filter(date__lt=current_datetime.date(), 
                                                          time__lt=current_datetime.time())
        count = expired_reservations.count()
        expired_reservations.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired reservations.'))
