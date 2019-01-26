from rest_framework.response import Response
from rest_framework.views import APIView

from river.apis.serializers import RiverSerializer
from river.models import River


class RiverView(APIView):
    def get(self, request, ):
        river = River.objects.last()
        serializer = RiverSerializer(river)
        return Response(serializer.data)
