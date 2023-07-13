from django.db import models


class Segment(models.Model):
    entity = models.ForeignKey('sampleapp.Entity', on_delete=models.CASCADE)
    ent = models.TextField()
    label = models.TextField()

    class JSONAPIMeta:
        resource_name = 'segments'
