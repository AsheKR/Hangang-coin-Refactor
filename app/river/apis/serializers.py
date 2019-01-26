from rest_framework import serializers

from river.models import River


class RiverSerializer(serializers.ModelSerializer):

    class Meta:
        model = River
        fields = (
            'temperature',
        )
