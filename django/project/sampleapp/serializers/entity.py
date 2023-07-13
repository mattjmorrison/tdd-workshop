from rest_framework_json_api import serializers
from sampleapp.models.entity import Entity


class EntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entity
        fields = ('sentence', )


class EntityV1Serializer(serializers.ModelSerializer):
    output = serializers.SerializerMethodField()

    def get_output(self, obj):
        output = []
        for segment in obj.segment_set.all():
            output.append({'ent': segment.ent, 'label': segment.label})
        return output

    class Meta:
        model = Entity
        fields = '__all__'
