from django.test import TestCase
from sampleapp.named_entity import NamedEntityClient
from sampleapp.tests.helpers import NerModelTestDouble


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
