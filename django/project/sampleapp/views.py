from django.views.generic import View
import json
from django.http import HttpResponse

from sampleapp.named_entity import NamedEntityClient
import spacy


class GetNamedEnts(View):

    def post(self, request):
        ner = spacy.load('en_core_web_sm')
        client = NamedEntityClient(ner)
        result = client.get_ents(request.POST['sentence'])
        response = {"entities": result.get('ents')}
        return HttpResponse(json.dumps(response))

