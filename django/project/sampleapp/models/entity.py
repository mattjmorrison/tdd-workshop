from django.db import models


class Entity(models.Model):
    sentence = models.TextField()

    class JSONAPIMeta:
        resource_name = 'entities'
