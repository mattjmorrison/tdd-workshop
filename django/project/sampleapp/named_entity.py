class NamedEntityClient:

    def __init__(self, model):
        self.model = model

    def get_ents(self, sent):
        doc = self.model(sent)
        entities = [{'ent': ent.text, 'label': self.map_label(ent.label_)} for ent in doc.ents]
        return {'ents': entities}

    def map_label(self, label):
        label_map = {
            'PERSON': 'Person',
            'NORP': 'Group',
            'LOC': 'Location',
            'GEP': 'Location',
            'LANGUAGE': 'Language',
        }
        return label_map[label]
