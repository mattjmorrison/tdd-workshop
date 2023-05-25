from django.db import models


class Entity(models.Model):
    sentence = models.TextField()
    results = models.JSONField()
