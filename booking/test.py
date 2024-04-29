from django.test import TestCase
from django.utils import timezone
from .models import User, Restaurant, Reservation
from datetime import timedelta
from django.urls import reverse

class ReservationTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a test restaurant
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test St",
            city="Testville",
            tt="123,456",
            type='S',
            capacity=10  # Set a capacity
        )


    def test_reservation_exceeding_capacity(self):
        # First reservation that fills capacity
        Reservation.objects.create(
            user=self.user,
            restaurant=self.restaurant,
            date=timezone.now().date() + timedelta(days=1),
            time=timezone.now().time(),
            number_of_people=10,
            is_active=True
        )
        # Another reservation that would exceed capacity
        response = self.client.post('/booking/reserve/', {
            'user': self.user.id,
            'restaurant': self.restaurant.id,
            'date': timezone.now().date() + timedelta(days=1),
            'time': (timezone.now() + timedelta(hours=1)).time(),  # Overlapping time
            'number_of_people': 1,
            'is_active': True
        })
        self.assertNotEqual(response.status_code, 302)

