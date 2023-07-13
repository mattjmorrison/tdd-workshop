from django.test import TestCase
import json
from sampleapp.models.entity import Entity


class Apiv1Tests(TestCase):

    def test_houston(self):
        response = self.client.post('/entity/', json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    "sentence": "Goodbye Houston"
                }
            }
        }), content_type='application/vnd.api+json')
        self.assertEqual(201, response.status_code, response.content)
        data = json.loads(response.content)
        self.assertEqual(
            data['data']['attributes']['output'],
            []
        )

    def test_ner_enpoint_given_json_body_with_known_entities_returns_entity_result_in_response(self):
        response = self.client.post('/entity/', json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    'sentence': 'Kamala Harris is vice president of the United States of America'
                }
            }
        }), content_type='application/vnd.api+json')
        self.assertEqual(201, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['data']['type'], "entities")
        self.assertEqual(
            data['data']['attributes']['sentence'],
            'Kamala Harris is vice president of the United States of America')
        self.assertEqual(
            data['data']['attributes']['output'],
            [
                {'ent': 'Kamala Harris', 'label': 'Person'},
                {'ent': 'the United States of America', 'label': 'Location'}
            ]
        )

    def test_get_existing_entity(self):
        e = Entity.objects.create(sentence='Hello Boston!')
        response = self.client.get(f'/entity/{e.pk}/', content_type='application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['data']['type'], "entities")
        self.assertEqual(data['data']['id'], str(e.pk))
        self.assertEqual(
            data['data']['attributes']['sentence'],
            'Hello Boston!')
        self.assertEqual(
            data['data']['attributes']['output'],
            [
                {'ent': 'Boston', 'label': 'Location'},
            ]
        )

    def test_updates_existing_entity(self):
        first = Entity.objects.create(sentence='Hello Boston!')
        response = self.client.patch(f'/entity/{first.pk}/', json.dumps({
            "data": {
                "id": first.pk,
                "type": "entities",
                "attributes": {
                    "sentence": "Goodbye Des Moines!"
                }
            }
        }), content_type='application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['data']['type'], "entities")
        self.assertEqual(data['data']['id'], str(first.pk))
        self.assertEqual(
            data['data']['attributes']['sentence'],
            'Goodbye Des Moines!')
        self.assertEqual(
            data['data']['attributes']['output'],
            [
                {'ent': 'Des Moines', 'label': 'Location'},
            ]
        )
        entities = Entity.objects.all()
        self.assertEqual(1, len(entities))
        entity = entities[0]
        self.assertEqual(entity.pk, first.pk)
        self.assertEqual(entity.sentence, 'Goodbye Des Moines!')

    def test_get_list_of_all_entities(self):
        first = Entity.objects.create(sentence='Hello Boston!')
        second = Entity.objects.create(sentence='Hello Des Moines!')
        response = self.client.get('/entity/', content_type='application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)['data']
        self.assertEqual(2, len(data))
        self.assertEqual(data[0]['type'], "entities")
        self.assertEqual(data[1]['type'], "entities")
        self.assertEqual(data[0]['id'], str(first.pk))
        self.assertEqual(data[1]['id'], str(second.pk))
        self.assertEqual(data[0]['attributes']['sentence'], first.sentence)
        self.assertEqual(data[1]['attributes']['sentence'], second.sentence)
        self.assertEqual(data[0]['attributes']['output'], [{'ent': 'Boston', 'label': 'Location'}])
        self.assertEqual(data[1]['attributes']['output'], [{'ent': 'Des Moines', 'label': 'Location'}])
