from django.views.generic import View
import json
from django.http import HttpResponse

from sampleapp.models import Entity


class GetNamedEnts(View):

    def post(self, request):
        sentence = json.loads(request.body)['data']['attributes']['sentence']
        entity = Entity.objects.create(sentence=sentence)
        return HttpResponse(json.dumps({
            "data": self._serialize(entity)
        }))

    def get(self, request, pk=None):
        if pk:
            entity = Entity.objects.get(pk=pk)
            return HttpResponse(json.dumps({
                'data': self._serialize(entity)
            }))
        else:
            return HttpResponse(json.dumps({
                'data': [self._serialize(e) for e in Entity.objects.all()]
            }))

    def _serialize(self, entity):
        return {
            'type': 'entities',
            'id': entity.pk,
            'attributes': {
                'sentence': entity.sentence,
                'results': entity.results,
            }
        }

    def delete(self, request, pk):
        Entity.objects.filter(pk=pk).delete()
        return HttpResponse(status=204)

    def patch(self, request, pk):
        entity = Entity.objects.get(pk=pk)
        entity.sentence = json.loads(request.body)['data']['attributes']['sentence']
        entity.save()
        return HttpResponse(json.dumps({
            'data': self._serialize(entity)
        }))
