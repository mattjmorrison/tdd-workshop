from django.db import models


class Entity(models.Model):
    sentence = models.TextField()
    legacy_output = models.JSONField(blank=True, default='[]', db_column='output')

    class JSONAPIMeta:
        resource_name = 'entities'
