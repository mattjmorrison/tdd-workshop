from django.db import models


class Segment(models.Model):
    entity = models.ForeignKey('sampleapp.Entity', on_delete=models.CASCADE)
    ent = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
