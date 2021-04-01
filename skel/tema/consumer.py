"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.name = kwargs['name']
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        """
        For every cart an id is assigned, then every command in that cart is analyzed
        Add or remove product until the quantity is met
        Sleep if add to cart or remove from cart can't be done, then sleep
        After doing all the commands for the cart, print the products
        """
        for cart in self.carts:
            cart_id = self.marketplace.new_cart()
            for cmd in cart:
                no_products_type = 0
                while no_products_type < cmd['quantity']:
                    check = False
                    if cmd['type'] == 'add':
                        check = self.marketplace.add_to_cart(cart_id, cmd['product'])
                    else:
                        check = self.marketplace.remove_from_cart(cart_id, cmd['product'])

                    if check or check is None:
                        no_products_type += 1
                    else:
                        time.sleep(self.retry_wait_time)

            products = self.marketplace.place_order(cart_id)
            for product in products:
                print('{} bought {}'.format(self.name, product))
