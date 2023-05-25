from django.views.generic import View
import json
from django.http import HttpResponse

from sampleapp.named_entity import NamedEntityClient
import spacy


class GetNamedEnts(View):

    def post(self, request):
        sentence = json.loads(request.body)['data']['attributes']['sentence']
        ner = spacy.load('en_core_web_sm')
        client = NamedEntityClient(ner)
        result = client.get_ents(sentence)
        return HttpResponse(json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    "sentence": sentence,
                    "results": result.get('ents')
                }
            }
        }))

