from django.db import models

from project.storages import HTTPStorage

class Media(models.Model):
    name = models.CharField(max_length=128)
    file = models.FileField(storage=HTTPStorage('http://localhost:5000/'))
