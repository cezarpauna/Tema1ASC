"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        # list of queues of producers (queue_producers[producer_id] = queue of producer_id)
        self.queue_producers = []
        # list of products in the marketplace
        self.products = []
        # maps product to producers
        self.producer_product = {}
        # list of carts (every car is a list of products)
        self.carts = []

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        producer_id = len(self.queue_producers)
        self.queue_producers.append([])

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.

        No need for lock because every thread has a different id
        """
        if self.queue_size_per_producer > len(self.queue_producers[producer_id]):
            self.products.append(product)
            self.producer_product[product] = producer_id
            self.queue_producers[producer_id].append(0)
            return True

        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        new_cart_id = len(self.carts)
        self.carts.append([])

        return new_cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again

        If we can add the product, decrement the queue of that producer,
        append the product to the cart and
        remove the product from the marketplace.
        """

        if product not in self.products:
            return False

        self.products.remove(product)
        self.carts[cart_id].append(product)
        # remove one element from queue of that producer
        if self.queue_producers[self.producer_product[product]]:
            self.queue_producers[self.producer_product[product]].pop(0)

        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.carts[cart_id].remove(product)
        self.products.append(product)
        # append one element to the queue of that producer (possible restriction for publish)
        self.queue_producers[self.producer_product[product]].append(0)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        products = self.carts[cart_id]
        return products
