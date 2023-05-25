from django.views.generic import View
import json
from django.http import HttpResponse

from sampleapp.models import Entity


class GetNamedEnts(View):

    def post(self, request):
        sentence = json.loads(request.body)['data']['attributes']['sentence']
        entity = Entity.objects.create(sentence=sentence)
        return HttpResponse(json.dumps({
            "data": {
                "id": entity.pk,
                "type": "entities",
                "attributes": {
                    "sentence": sentence,
                    "results": entity.results
                }
            }
        }))

