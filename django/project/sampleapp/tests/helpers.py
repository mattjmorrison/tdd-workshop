
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
