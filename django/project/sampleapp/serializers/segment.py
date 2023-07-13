from rest_framework_json_api import serializers
from sampleapp.models.segment import Segment


class SegmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Segment
        fields = '__all__'

