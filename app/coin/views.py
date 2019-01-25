from django.shortcuts import render


# Create your views here.
from coin.models import Coin
from river.models import River


def home_page(request):
    coin = Coin.objects.first()
    coin_list = Coin.CURRENCY_PAIR
    river = None

    try:
        if coin.latest_value < coin.today_master_value:
            river = River.objects.last()
            if river is None:
                raise AttributeError
    except AttributeError:
        return render(request, 'wait.html', )

    return render(request, 'home.html', context={
        'coin': coin,
        'coin_list': coin_list,
        'river': river
    })
