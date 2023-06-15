from django.db.models.signals import pre_save
from sampleapp.named_entity import NamedEntityClient
from sampleapp.models import Entity
from django.dispatch import receiver
import spacy


@receiver(pre_save, sender=Entity)
def process_entity(sender, instance, **kwargs):
    ner = spacy.load('en_core_web_sm')
    client = NamedEntityClient(ner)
    instance.output = client.get_ents(instance.sentence)['ents']

