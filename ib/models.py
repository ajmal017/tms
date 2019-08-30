from django.db import models

# Create your models here.

# date
# url
# symbol
# volume
# direction
#
# order_place_date
# order_status
# order_type
# order_id
# order_place_response
# order_execution_response
# order_execution_price


class Signal(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    url = models.CharField(max_length=50, null=True, blank=True)
    symbol = models.CharField(max_length=10, null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    direction = models.CharField(max_length=10, null=True, blank=True)
    order_place_date = models.DateTimeField(null=True, blank=True)
    order_status = models.CharField(max_length=20, null=True, blank=True)
    order_type = models.CharField(max_length=10, null=True, blank=True)
    order_id = models.CharField(max_length=40, null=True, blank=True)
    order_place_response = models.TextField(null=True, blank=True)
    order_execution_response = models.TextField(null=True, blank=True)
    order_execution_price = models.IntegerField(null=True, blank=True)

    # Pretty name output in console
    def __str__(self):
        return self.url + ' - ' + self.symbol