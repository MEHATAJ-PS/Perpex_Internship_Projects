from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SimpleMenuView(APIView):
    """
    A temporary endpoint to serve a static menu list.
    Will be replaced with DB-driven data in the future.
    """
    def get(self, request):
        """
        Returns a static list of menu items with name, description, and price.
        """
        menu = [
            {"name":"Veg Biryani", "description": "Spicy rice with vegetables", "price": 120.00},
            {"name": "Butter Naan", "description": "Tandoori naan with butter", "price": 40.00},
            {"name": "Paneer Tikka", "description": "Grilled cottage cheese cubes", "price": 150.00},
            {"name": "Margherita Pizza", "description":"Classic pizza with tomato sauce and mozzarella cheese.", "price": 299.00},
            {"name": "Pasta Alfredo", "description": "Creamy pasta with rich Alfredo sauce and mushrooms.", "price": 349.00},
            {"name": "Caesar Salad", "description": "Fresh romaine lettuce with Caesar dressing and croutons.", "price": 199.00}
        ]
        return Response(menu, status=status.HTTP_200_OK)