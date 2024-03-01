from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import  Room
from .serializers import Roomserializer

@api_view(['GET'])
def getrooms(request):
    room=Room.objects.all()
    serializ=Roomserializer(room, many=True)
    return Response(serializ.data)

@api_view(['GET'])
def getroom_by_id(request,pk):
    rooms=Room.objects.get(id=pk)
    serializ=Roomserializer(rooms,many=False)
    return Response(serializ.data)