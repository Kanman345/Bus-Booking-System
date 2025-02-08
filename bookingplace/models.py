from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('passenger', 'Passenger'),
        ('admin', 'Administrator'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='passenger')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class Route(models.Model):
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.start_location} → {self.end_location}"


 
class Bus(models.Model):
    bus_number = models.CharField(max_length=10, unique=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    total_seats = models.PositiveIntegerField
    available_seats = models.PositiveIntegerField
    departure_time = models.DateTimeField
    arrival_time = models.DateTimeField

    def __str__(self):
        return f"{self.bus_number} - {self.route_name}"
    

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_count = models.PositiveIntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])

    def save(self, *args, **kwargs):
        if self.bus.available_seats >= self.seat_count:
            self.bus.available_seats -= self.seat_count
            self.bus.save()
            super().save(*args, **kwargs)
        else:
            raise ValueError("Not enough seats available")

    def __str__(self):
        return f"Booking {self.id} by {self.user.username} on {self.bus.bus_number}"
    
class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('add', 'Add Funds'), ('pay', 'Payment')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} by {self.user.username}"



    



