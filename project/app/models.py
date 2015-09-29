from django.db import models

from project.storages import HTTPStorage

class Media(models.Model):
    name = models.CharField(max_length=128)
    file = models.ImageField(
        storage=HTTPStorage('http://localhost:5000/'),
        width_field='width',
        height_field='height')
    width = models.PositiveIntegerField(editable=False)
    height = models.PositiveIntegerField(editable=False)
