from rest_framework.response import Response
from rest_framework.views import APIView

from coin.apis.serializers import CoinSerializer
from coin.models import Coin


class CoinView(APIView):
    def get(self, request, coin, ):
        coin = Coin.objects.get(name=coin)
        serializer = CoinSerializer(coin)
        return Response(serializer.data)
