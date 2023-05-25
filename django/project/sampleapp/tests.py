from django.test import TestCase
import json
from sampleapp.named_entity import NamedEntityClient


class NerModelTestDouble:

    def __init__(self, model):
        pass

    def returns_doc_ents(self, ents):
        self.ents = ents

    def __call__(self, sent):
        return DocTestDouble(sent, self.ents)


class DocTestDouble:

    def __init__(self, sent, ents):
        self.ents = [SpanTestDouble(ent['text'], ent['label_']) for ent in ents]


class SpanTestDouble:

    def __init__(self, text, label):
        self.text = text
        self.label_ = label


class Test(TestCase):

    def test_empty_string(self):
        model = NerModelTestDouble('eng')
        model.returns_doc_ents([])
        ner = NamedEntityClient(model)
        ents = ner.get_ents("")
        self.assertIsInstance(ents, dict)

    def test_non_empty_string(self):
        model = NerModelTestDouble('eng')
        model.returns_doc_ents([])
        ner = NamedEntityClient(model)
        ents = ner.get_ents("Madison is a city in Wisconnsin")
        self.assertIsInstance(ents, dict)

    def test_person_returned(self):
        model = NerModelTestDouble('eng')
        model.returns_doc_ents([{'text': 'Laurrent Fressinet', 'label_': 'PERSON'}])
        ner = NamedEntityClient(model)
        result = ner.get_ents("...")
        expected_result = {'ents': [{'ent': 'Laurrent Fressinet', 'label': 'Person'}], 'html': ''}
        self.assertListEqual(result['ents'], expected_result['ents'])


class ApiTests(TestCase):

    def test_ner_endpoint_given_json_body_returns_200(self):
        response = self.client.post('/entity/', json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    "sentence": "Steve Malkmus is in a good band."
                }
            }
        }), content_type='application/vnd.api+json')
        self.assertEqual(200, response.status_code)

    def test_ner_enpoint_given_json_body_with_known_entities_returns_entity_result_in_response(self):
        response = self.client.post('/entity/', json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    'sentence': 'Kamala Harris is vice president of the United States of America'
                }
            }
        }), content_type='application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data, {
            "data": {
                "type": "entities",
                "attributes": {
                    'sentence': 'Kamala Harris is vice president of the United States of America',
                    'results': [
                        {'ent': 'Kamala Harris', 'label': 'Person'},
                        {'ent': 'the United States of America', 'label': 'Location'}
                    ]
                }
            }
        })

    def test_results_are_saved_in_database(self):
        response = self.client.post('/entity/', json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    'sentence': 'Kamala Harris is vice president of the United States of America'
                }
            }
        }), content_type='application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        pk = json.loads(response.content)['data']['id']
        entity = Entity.objects.get(pk=pk)
        self.assertEqual(entitiy.sentence, 'Kamala Harris is vice president of the United States of America')
        self.assertEqual(entitiy.results, ([
            {'ent': 'Kamala Harris', 'label': 'Person'},
            {'ent': 'the United States of America', 'label': 'Location'}
        ]))
