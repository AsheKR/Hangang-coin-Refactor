from django.shortcuts import render


# Create your views here.
from coin.models import Coin


def home_page(request):
    coin = Coin.objects.first()

    if not coin:
        return render(request, 'wait.html', )

    try:
        master_value = coin.today_master_value
        now_value = coin.latest_value
    except AttributeError:
        return render(request, 'wait.html', )

    return render(request, 'home.html', context={
        'coin': coin,

    })
