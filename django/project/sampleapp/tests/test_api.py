from django.test import TestCase
import json
from sampleapp.models.entity import Entity


class ApiTests(TestCase):

    def test_houston(self):
        response = self.client.post('/entity/', json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    "sentence": "Goodbye Houston"
                }
            }}),
            content_type='application/vnd.api+json',
            HTTP_X_IMTAPPS_API_VERSION='2.0'
        )
        self.assertEqual(201, response.status_code, response.content)
        data = json.loads(response.content)
        self.assertNotIn('output', data['data']['attributes'])

    def test_ner_endpoint_given_json_body_returns_200(self):
        response = self.client.post('/entity/?include=segments', json.dumps({
            "data": {
                "type": "entities",
                "attributes": {
                    "sentence": "Steve Malkmus is in a good band."
                }
            }
        }), content_type='application/vnd.api+json')
        self.assertEqual(201, response.status_code, response.content)
        self.fail(response.content)

    def test_delete_existing_entity(self):
        e = Entity.objects.create(sentence='Hello Boston!')
        response = self.client.delete(f'/entity/{e.pk}/', content_type='application/vnd.api+json')
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Entity.objects.filter(pk=e.pk).count())

    def test_only_deletes_what_was_requested(self):
        first = Entity.objects.create(sentence='Hello Boston!')
        second = Entity.objects.create(sentence='Hello Philly!')
        response = self.client.delete(f'/entity/{first.pk}/', content_type='application/vnd.api+json')
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Entity.objects.filter(pk=first.pk).count())
        self.assertEqual(1, Entity.objects.filter(pk=second.pk).count())
