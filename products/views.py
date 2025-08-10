from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer



class ItemView(APIView):
    """
    API endpoint to retrieve and create items stored in the database.
    """

    def get(self, request):
        """
        Handle GET requests to return all items from the database.
        """
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle POST requests to create a new item.
        """
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MenuAPIView(APIView):
    """
    API endpoint to retrieve the restaurant's hardcode menu.
    """
    def get(self, request):
        """
        Return a static list of dishes with name, description, and price.
        """
        menu_data = [
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

            },
            {

                "name": "Margherita Pizza",
                "description": "Classic pizza with tomato sauce and mozzarella cheese.",
                "price": 299.00

            },
            {

                "name": "Pasta Alfredo",
                "description": "Creamy pasta with rich Alfredo sauce and mushrooms.",
                "price": 349.00

            },
            {

                "name": "Caesar Salad",
                "description": "Fresh romaine lettuce with Caesar dressing and croutons.",
                "price": 199.00
                
            }
        ]
        return Response(menu_data, status=status.HTTP_200_OK)
