from django.core.management.base import BaseCommand, CommandError
from ib.models import Signal
import time
from random import randrange

class Request(BaseCommand):

    @staticmethod
    def store():
        record = Signal(
            date=time.strftime('%Y-%m-%d %H:%M:%S'),
            url="test_url",
            symbol="aapl",
            volume=150,
            direction="long",
            order_place_date=time.strftime('%Y-%m-%d %H:%M:%S'),
            order_status="test",
            order_type="market",
            order_id=randrange(100000)
        )
        record.save()



