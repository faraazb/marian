import uuid

from django.core.validators import RegexValidator
from django.db import models


class Pickup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter phone number in format: '+999999999'. "
                                                                   "Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    address = models.TextField()
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    is_done = models.BooleanField(default=False)

    REQUIRED_FIELDS = [name, phone_number, description]

    objects = models.Manager()

    class Meta:
        ordering = ["-update_time"]
