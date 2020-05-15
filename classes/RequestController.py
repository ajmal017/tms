# Receives requests from urls.py
# Adds a request to DB
# Runs a loop which waits for the response to be written to DB

from django.http import HttpResponse
from classes.Request import Request
import os.path
import logging # Default logger
import json
import time
import datetime
from ib.models import Signal

import sys
sys.path.insert(1, 'classes/')  # Path to DbLogger.py # Works good
from DbLogger import DbLogger

class PlaceOrder:

    errorMessage = 'Error: Request is in progress. You can not send more than one request at a time.<br>' \
                   'Possible problem 1: requests are not handled with IB and no response is received form IB Gateway.<br>'\
                   'Possible problem 2: IB Gateway is not connected. Check the status in VNC.<br>' \
                   'Please delete all pending tasks manually in order to continue.<br>'\
                   + str(datetime.datetime.now())

    @staticmethod
    def botstatus(request):

        PlaceOrder.SetupLogger('error from bot status')


        # If there are pending tasks active
        if PlaceOrder.isLock(request): return HttpResponse(PlaceOrder.errorMessage)

        requestPayload = json.dumps({
            "url": "botstatus"
        })

        # Add a record to bd
        res = PlaceOrder.store(requestPayload)

        # loop here. Wait 20 sec
        for i in range(20):
            record = Signal.objects.get(id=res.id)
            print(record)
            if record.response_payload != None:
                return HttpResponse('Bot time: ' + str(datetime.datetime.now()) + '<br> Status: ' + record.response_payload)
            time.sleep(1)

        return HttpResponse('Bot status timeout error. Response from the exchange has not been received within 10 seconds. ' + str(datetime.datetime.now()))


    @staticmethod
    def placeorder(request, order_type, exchange, symbol, volume, direction, currency, price=""):

        # If there are pending tasks active
        if PlaceOrder.isLock(request): return HttpResponse(PlaceOrder.errorMessage)

        requestPayload = json.dumps({
            "url": "placeorder",
            "order_type": order_type,
            "exchange": exchange,
            "symbol": symbol,
            "currency": currency,
            "volume": volume,
            "price": price,
            "direction": direction,
            "status": "new"
        })

        # Add a record to bd
        res = PlaceOrder.store(requestPayload)

        # loop here. Wait 20 sec
        for i in range(20):
            record = Signal.objects.get(id=res.id) # Check the created record
            print(record)
            if record.response_payload != None:
                return HttpResponse(
                    'Bot time: ' + str(datetime.datetime.now()) + '<br> Status: ' + record.response_payload)
            time.sleep(1)

        # Release the lock
        return HttpResponse(
            'Place timeout error. Response from the exchange has not been received within 10 seconds. ' + str(
                datetime.datetime.now()))

    @staticmethod
    def getquote(request, exchange, symbol, currency):

        # If there are pending tasks active
        if PlaceOrder.isLock(request): return HttpResponse(PlaceOrder.errorMessage)

        requestPayload = json.dumps({
            "url": "getquote",
            "exchange": exchange,
            "symbol": symbol,
            "currency": currency,
            "status": "new"
        })

        # Add a record to bd
        res = PlaceOrder.store(requestPayload)

        # loop here. Wait 20 sec
        for i in range(20):
            record = Signal.objects.get(id=res.id)
            print(record)
            if record.response_payload != None:
                return HttpResponse('Bot time: ' + str(datetime.datetime.now()) + '<br> Quote: ' + record.response_payload)
            time.sleep(1)

        return HttpResponse(
            'Getquote status timeout error. Response from the exchange has not been received within 10 seconds. ' + str(datetime.datetime.now()))

    @staticmethod
    def cancelallorders(request):

        # If there are pending tasks active
        if PlaceOrder.isLock(request): return HttpResponse(PlaceOrder.errorMessage)

        requestPayload = json.dumps({
            "url": "cancelall"
        })

        # Add a record to bd
        res = PlaceOrder.store(requestPayload)

        # loop here. Wait 20 sec
        for i in range(20):
            record = Signal.objects.get(id=res.id)
            print(record)
            if record.response_payload != None:
                # Return only price
                return HttpResponse(
                    'Bot time: ' + str(datetime.datetime.now()) + '<br> Cancel all: ' + record.response_payload)
            time.sleep(1)

        return HttpResponse(
            'Cancel all timeout error. Response from the exchange has not been received within 10 seconds. ' + str(datetime.datetime.now()))

    @staticmethod
    def getpositions(request, symbol=""):

        # If there are pending tasks active
        if PlaceOrder.isLock(request): return HttpResponse(PlaceOrder.errorMessage)

        requestPayload = json.dumps({
            "url": "getpositions",
            "symbol": symbol
        })

        # Add a record to bd
        res = PlaceOrder.store(requestPayload)

        # loop here. Wait 20 sec
        for i in range(20):
            record = Signal.objects.get(id=res.id)
            print(record)
            if record.response_payload != None:
                # Return only price
                return HttpResponse(
                    'Bot time: ' + str(datetime.datetime.now()) + '<br> Get positions: ' + record.response_payload)
            time.sleep(1)

        return HttpResponse(
            'Getorders timeout error. Response from the exchange has not been received within 10 seconds. ' + str(
                datetime.datetime.now()))

    @staticmethod
    def isLock(request):
        if Signal.objects.filter(status='pending').count() != 0:
            return True
        else:
            return False

    @staticmethod
    def store(requestPayload):

        try:
            return Request.store(requestPayload)
        except:
            error = 'RequestController.py. Update Model query error. Most likely - no MYSQL connection. Code: 43ee'
            print(error)
            #self.log.error(error)

    @staticmethod
    def SetupLogger(error):
        if not os.path.exists("log"):
            os.makedirs("log")

        time.strftime("pyibapi.%Y%m%d_%H%M%S.log")
        recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(filename)s:%(lineno)d %(message)s'
        timefmt = '%y%m%d_%H:%M:%S'

        logdb = DbLogger()
        logging.basicConfig(level=logging.DEBUG, format=recfmt, datefmt=timefmt)  # level=logging.INFO
        logging.getLogger('').addHandler(logdb)

        logging.getLogger('MY_LOGGER').setLevel('DEBUG')
        logging.getLogger('MY_LOGGER').error(error)

    def __delete__(self):
        return HttpResponse("")
