"""tms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.contrib import admin
from django.urls import path
from classes.RequestController import PlaceOrder  # Class reference

urlpatterns = [
    path('admin/', admin.site.urls),

    # Bot status
    # http://127.0.0.1:8000/botstatus
    path('botstatus', PlaceOrder.botstatus),

    # Place limit order.
    # Place a limit/market order - the same placeorder controller is used / RequestController.py
    # http://127.0.0.1:8000/placeorder/limit/nyse/iag/usd/1/buy/2
    path('placeorder/<order_type>/<exchange>/<symbol>/<currency>/<volume>/<direction>/<price>', PlaceOrder.placeorder),

    # Place market order
    # http://127.0.0.1:8000/placeorder/market/nyse/iag/usd/1/buy
    path('placeorder/<order_type>/<exchange>/<symbol>/<currency>/<volume>/<direction>', PlaceOrder.placeorder),

    # Get quote
    path('getquote/<exchange>/<symbol>/<currency>', PlaceOrder.getquote),

    # Cancel all placed orders. Including market orders if they are placed during non trading hours
    # http://127.0.0.1:8000/cancelall
    path('cancelall', PlaceOrder.cancelallorders),

    # Get positions
    path('getpositions', PlaceOrder.getpositions),

    # Get positions for symbol
    path('getpositions/<symbol>', PlaceOrder.getpositions)
]
