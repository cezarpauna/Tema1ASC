"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.producer_id = self.marketplace.register_producer()

    def run(self):
        """
        Producers adds products to the marketplace
        If the product can be added then sleep for the given amount of time
        If not sleep for the amount of time specified in init (republish wait time)
        """
        while 1:
            for (product, number, time_sleep_normal) in self.products:
                index_prod = 0
                while index_prod < number:
                    can_publish = self.marketplace.publish(self.producer_id, product)
                    if can_publish:
                        time.sleep(time_sleep_normal)
                        index_prod += 1
                    else:
                        time.sleep(self.republish_wait_time)
