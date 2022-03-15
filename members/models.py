from django.db import models
from django.db.models.fields.files import ImageField

class Modulos(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    image=models.ImageField(upload_to='images/')
    direccion = models.CharField(max_length=500, blank=True, null=True)

