from django.views.generic import View
import json
from django.http import HttpResponse

from sampleapp.named_entity import NamedEntityClient
from sampleapp.models import Entity
import spacy


class GetNamedEnts(View):

    def post(self, request):
        sentence = json.loads(request.body)['data']['attributes']['sentence']
        ner = spacy.load('en_core_web_sm')
        client = NamedEntityClient(ner)
        result = client.get_ents(sentence)
        entity = Entity.objects.create(sentence=sentence, results=result.get('ents'))
        return HttpResponse(json.dumps({
            "data": {
                "id": entity.pk,
                "type": "entities",
                "attributes": {
                    "sentence": sentence,
                    "results": result.get('ents')
                }
            }
        }))

