from rest_framework import serializers

from coin.models import Coin


class CoinSerializer(serializers.ModelSerializer):
    coin_name = serializers.SerializerMethodField()
    latest_value = serializers.SerializerMethodField()
    today_master_value = serializers.SerializerMethodField()
    percent = serializers.SerializerMethodField()

    class Meta:
        model = Coin
        fields = (
            'coin_name',
            'latest_value',
            'today_master_value',
            'percent',
        )

    def get_coin_name(self, obj):
        return obj.name

    def get_latest_value(self, obj):
        return obj.latest_value

    def get_today_master_value(self, obj):
        return obj.today_master_value

    def get_percent(self, obj):
        percent = ((obj.latest_value / obj.today_master_value) - 1) * 100
        return float('{0:.2f}'.format(percent))