import os
import random

from django.conf import settings
from rest_framework import serializers

from coin.models import Coin


class CoinSerializer(serializers.ModelSerializer):
    coin_name = serializers.SerializerMethodField()
    latest_value = serializers.SerializerMethodField()
    today_master_value = serializers.SerializerMethodField()
    percent = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Coin
        fields = (
            'coin_name',
            'latest_value',
            'today_master_value',
            'percent',
            'image',
        )

    def get_coin_name(self, obj):
        return obj.name

    def get_latest_value(self, obj):
        return obj.latest_value

    def get_today_master_value(self, obj):
        return obj.today_master_value

    def get_percent(self, obj):
        return obj.percent

    def get_image(self, obj):
        if obj.percent < 0:
            dir_name = 'down'
            if obj.percent < -15:
                # -15보다 낮은것
                folder_name = '-20_-15'
            elif obj.percent < -10:
                # -10보다 낮은것
                folder_name = '-15_-10'
            else:
                folder_name = '-10_0'
        else:
            dir_name = 'up'
            if obj.percent < 10:
                # 10보다 낮은 것
                folder_name = 'p0_10'
            elif obj.percent < 15:
                # 15보다 낮은것
                folder_name = 'p10_15'
            else:
                folder_name = 'p15_20'

        dir_path = os.path.join(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), dir_name), folder_name)

        image_files = os.listdir(dir_path)
        img_file = random.choice(image_files)

        img_full_path = os.path.join(dir_path, img_file)
        img_rel_path = img_full_path.split('app')[1]

        return img_rel_path
