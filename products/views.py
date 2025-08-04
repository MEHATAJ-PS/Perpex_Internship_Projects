from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Item
from .serializers import ItemSerializer


#-----------------------------
# Dynamic Menu (from database)
#-----------------------------
class ItemView(APIView):

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#-------------------------
# Static Menu (hardcoded)
#-------------------------
class MenuAPIView(APIView):
    def get(self.request):
        menu = [
            {
                "name": "Veg Biryani",
                "description": "Spicy rice with vegetables",
                "price": 120.00
            },
            {
                "name": "Butter Naan",
                "description": "Tandoori naan with butter",
                "price": 40.00
            },
            {
                "name": "Paneer Tikka",
                "description": "Grilled cottage cheese cubes",
                "price": 150.00
            }
        ]
        return Response(menu, status=status.HTTP_200_OK)
