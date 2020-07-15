from django.db import models
from django.utils import timezone

DEFAULT_EXPIRY_DAYS = 30  # in days


def get_default_expiry():
    return timezone.now() + timezone.timedelta(days=DEFAULT_EXPIRY_DAYS)


class UrlShortnerModel(models.Model):
    """
    Stores short string vs actual url in the database
    """
    short_url = models.CharField(max_length=64, unique=True)
    actual_url = models.CharField(max_length=255, unique=False)
    expiry_date = models.DateTimeField(default=get_default_expiry)
    created_on = models.DateTimeField(auto_now=True)
