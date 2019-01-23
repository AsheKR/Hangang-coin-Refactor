from django.contrib import admin

# Register your models here.
from coin.models import CoinValue, Coin

admin.site.register(Coin)
admin.site.register(CoinValue)