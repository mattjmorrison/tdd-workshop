from django.db.models.signals import post_save
from sampleapp.named_entity import NamedEntityClient
from sampleapp.models.entity import Entity
from sampleapp.models.segment import Segment
from django.dispatch import receiver
import spacy


@receiver(post_save, sender=Entity)
def process_entity(sender, instance, **kwargs):
    ner = spacy.load('en_core_web_sm')
    client = NamedEntityClient(ner)
    instance.segment_set.all().delete()
    for segment in client.get_ents(instance.sentence)['ents']:
        Segment.objects.create(entity=instance, ent=segment['ent'], label=segment['label'])

