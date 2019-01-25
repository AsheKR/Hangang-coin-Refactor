from django.shortcuts import render


# Create your views here.
from coin.models import Coin
from river.models import River


def home_page(request, coin=None):
    coin_list = Coin.objects.all()
    river = None

    try:
        if not coin:
            coin = Coin.objects.first()
        else:
            coin = Coin.objects.filter(name=coin)[0]

        if coin.latest_value < coin.today_master_value:
            river = River.objects.last()
            if river is None:
                raise AttributeError
    except (AttributeError, IndexError):
        return render(request, 'wait.html', )

    return render(request, 'home.html', context={
        'coin': coin,
        'coin_list': coin_list,
        'river': river
    })
