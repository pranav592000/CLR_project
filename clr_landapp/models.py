from django.db import models
from django.contrib.auth.models import User

class UploadedFile(models.Model):
    name = models.CharField(max_length=255)
    FileField = models.FileField(upload_to='uploads/')
    tag = models.CharField(max_length=50, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PrinterConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    printer_name = models.CharField(max_length=255)
    duplex = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
