from django.db import models


# Create your models here.
class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    path = models.CharField(max_length=2048)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} at {self.timestamp} -> {self.path}"


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.ip_address


class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.TextField()

    def __str__(self):
        return f'{self.ip_address}, {self.reason}'
