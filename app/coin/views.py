from django.shortcuts import render


# Create your views here.
from coin.models import Coin


def home_page(request):
    coin = Coin.objects.first()

    return render(request, 'home.html', context={
        'coin': coin,
    })
