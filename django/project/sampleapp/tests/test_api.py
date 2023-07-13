from django.test import TestCase
import json
from sampleapp.models.entity import Entity


class Apiv2Tests(TestCase):

    def test_ner_endpoint_given_json_body_returns_200(self):
        response = self.client.post('/entity/', json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    "sentence": "Steve Malkmus is in a good band."
                }
            }
        }),
        content_type='application/vnd.api+json',
        HTTP_X_IMTAPPS_API_VERSION='2.0')
        self.assertEqual(201, response.status_code, response.content)
        data = json.loads(response.content)
        self.assertNotIn('output', data['data']['attributes'])

    def test_ner_enpoint_given_json_body_with_known_entities_returns_entity_result_in_response(self):
        response = self.client.post('/entity/', json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    'sentence': 'Kamala Harris is vice president of the United States of America'
                }
            }
        }), content_type='application/vnd.api+json',
        HTTP_X_IMTAPPS_API_VERSION='2.0')
        self.assertEqual(201, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['data']['type'], "entities")
        self.assertEqual(
            data['data']['attributes']['sentence'],
            'Kamala Harris is vice president of the United States of America')

    def test_results_are_saved_in_database(self):
        response = self.client.post('/entity/', json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    'sentence': 'Kamala Harris is vice president of the United States of America'
                }
            }
        }),
        content_type='application/vnd.api+json',
        HTTP_X_IMTAPPS_API_VERSION='2.0')
        self.assertEqual(201, response.status_code)
        pk = json.loads(response.content)['data']['id']
        entity = Entity.objects.get(pk=pk)
        self.assertEqual(entity.sentence, 'Kamala Harris is vice president of the United States of America')
        segments = entity.segment_set.all().order_by('label')
        self.assertEqual(2, len(segments))
        s1, s2 = segments
        self.assertEqual(s1.ent, 'the United States of America')
        self.assertEqual(s1.label, 'Location')
        self.assertEqual(s2.ent, 'Kamala Harris')
        self.assertEqual(s2.label, 'Person')

    def test_get_existing_entity(self):
        e = Entity.objects.create(sentence='Hello Boston!')
        response = self.client.get(
            f'/entity/{e.pk}/',
            content_type='application/vnd.api+json',
            HTTP_X_IMTAPPS_API_VERSION='2.0')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['data']['type'], "entities")
        self.assertEqual(data['data']['id'], str(e.pk))
        self.assertEqual(
            data['data']['attributes']['sentence'],
            'Hello Boston!')

    def test_delete_existing_entity(self):
        e = Entity.objects.create(sentence='Hello Boston!')
        response = self.client.delete(
            f'/entity/{e.pk}/',
            content_type='application/vnd.api+json',
            HTTP_X_IMTAPPS_API_VERSION='2.0')
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Entity.objects.filter(pk=e.pk).count())

    def test_only_deletes_what_was_requested(self):
        first = Entity.objects.create(sentence='Hello Boston!')
        second = Entity.objects.create(sentence='Hello Philly!')
        response = self.client.delete(
            f'/entity/{first.pk}/',
            content_type='application/vnd.api+json',
            HTTP_X_IMTAPPS_API_VERSION='2.0')
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Entity.objects.filter(pk=first.pk).count())
        self.assertEqual(1, Entity.objects.filter(pk=second.pk).count())

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
        }),
        HTTP_X_IMTAPPS_API_VERSION='2.0',
        content_type='application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(data['data']['type'], "entities")
        self.assertEqual(data['data']['id'], str(first.pk))
        self.assertEqual(
            data['data']['attributes']['sentence'],
            'Goodbye Des Moines!')
        entities = Entity.objects.all()
        self.assertEqual(1, len(entities))
        entity = entities[0]
        self.assertEqual(entity.pk, first.pk)
        self.assertEqual(entity.sentence, 'Goodbye Des Moines!')
        self.assertEqual(
            [{'ent': e.ent, 'label': e.label} for e in entity.segment_set.all()],
            [{'ent': 'Des Moines', 'label': 'Location'}]
        )

    def test_get_list_of_all_entities(self):
        first = Entity.objects.create(sentence='Hello Boston!')
        second = Entity.objects.create(sentence='Hello Des Moines!')
        response = self.client.get(
            '/entity/',
            HTTP_X_IMTAPPS_API_VERSION='2.0',
            content_type='application/vnd.api+json')
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)['data']
        self.assertEqual(2, len(data))
        self.assertEqual(data[0]['type'], "entities")
        self.assertEqual(data[1]['type'], "entities")
        self.assertEqual(data[0]['id'], str(first.pk))
        self.assertEqual(data[1]['id'], str(second.pk))
        self.assertEqual(data[0]['attributes']['sentence'], first.sentence)
        self.assertEqual(data[1]['attributes']['sentence'], second.sentence)
