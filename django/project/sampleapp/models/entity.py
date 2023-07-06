from django.db import models


class Entity(models.Model):
    sentence = models.TextField()
    output = models.JSONField(blank=True)

    class JSONAPIMeta:
        resource_name = 'entities'
