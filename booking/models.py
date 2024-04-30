from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Define your custom user model
class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

# Define the Restaurant model
class Restaurant(models.Model):
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Corrected from on_related to on_delete
        null=True,
        blank=True,
        related_name='managed_restaurants'
    )
    TYPE_CHOICES = (
        ('S', 'Solidaire'),  # 'S' for Solidaire
        ('E', 'Economique'),  # 'E' for Economique
    )
    
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    tt = models.CharField(max_length=100)  # Assuming 'tt' is a coordinate in string format
    type = models.CharField(max_length=1, choices=(('S', 'Solidaire'), ('E', 'Economique')))
    capacity = models.IntegerField(default=0)  # Default capacity
    description = models.TextField(default="No description available")  # Default description

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations")
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    number_of_people = models.IntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)  # Indicates if the reservation is active or cancelled

    def __str__(self):
        return f"{self.user} reservation at {self.restaurant} on {self.date} at {self.time}"


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews')
    text = models.TextField()
    rating = models.IntegerField(default=0, choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} review of {self.restaurant.name}: {self.rating}/5"


class ConversationManager(models.Manager):
    def get_or_create_participants(self, user1, user2):
        conversation = self.filter(participants=user1).filter(participants=user2)
        if conversation.exists():
            return conversation.first(), False
        else:
            conversation = self.create()
            conversation.participants.add(user1, user2)
            return conversation, True

class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    objects = ConversationManager()


    def get_other_participant(self, user):
        return self.participants.exclude(id=user.id).first().username


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {} to {} at {}".format(self.sender, self.conversation, self.timestamp)
    
    
    
