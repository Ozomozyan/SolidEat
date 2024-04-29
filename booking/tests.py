from django.test import TestCase
from django.utils import timezone
from .models import User, Restaurant, Reservation
from datetime import timedelta

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
            capacity=10  # Set a known capacity
        )

    def test_reservation_within_capacity(self):
        # Create reservation data to post
        reservation_data = {
            'date': timezone.now().date() + timedelta(days=1),  # Reservation for tomorrow
            'time': '12:00',  # Assuming time field accepts this format
            'number_of_people': 5,
            'special_requests': 'None'
        }
        # Login as the test user before making the post request
        self.client.login(username='testuser', password='12345')
        # Post data to the reservation URL
        # Try to make another reservation that would exceed capacity
        response = self.client.post(
            f'/booking/restaurant/{self.restaurant.id}/reserve/',
            {
                'date': timezone.now().date() + timedelta(days=1),
                'time': '12:00',
                'number_of_people': 11,
                'special_requests': 'None'
            }
        )
        self.assertNotEqual(response.status_code, 200)  # Ensure failure



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
        # Try to make another reservation that would exceed capacity
        response = self.client.post(
            f'/booking/restaurant/{self.restaurant.id}/reserve/',  # Correct URL based on urlpatterns
            {
                'date': timezone.now().date() + timedelta(days=1),
                'time': '13:00',  # Different time to avoid overlap
                'number_of_people': 10,
                'special_requests': 'None'
            }
        )
        self.assertNotEqual(response.status_code, 200)  # Ensure failure

