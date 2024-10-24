import sys
import logging
from pandas import read_csv, DataFrame
from collections import defaultdict
import enum
import queue
import time

logging.basicConfig(
    filename='logfile.log',
    # stream=sys.stdout,
    format="%(asctime)s - %(name)s [lineno %(lineno)4d] - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__file__)


class Side(enum.Enum):
    BUY = 0
    SELL = 1


def get_timestamp():
    """ Microsecond timestamp """
    return int(1e6 * time.time())


class Order:
    def __init__(self, side, price, size, order_id=None, timestamp=None):
        self.side = side
        self.price = price
        self.size = size
        self.timestamp = timestamp
        self.order_id = order_id

    def __repr__(self):
        return f"{self.side} {self.size} units at {self.price}"


class OrderBook:
    def __init__(self):
        """Initialize order book attributes"""
        self.bids = defaultdict(list) # Dictionary to store buy side orders
        self.offers = defaultdict(list) # Dictionary to store sell side orders
        self.order_ids = {}

    def apply_delta(self, order):
        """Determine the type of order event and call the appropriate function
        add_order, delete_order, update_order
        """
        side = Side.BUY if order.orderSide == 'B' else Side.SELL
        incoming_order = Order(side, order.px, order.qty, order.orderId)
        incoming_order.timestamp = get_timestamp()

        if incoming_order.price == 0:
            self._delete_order(incoming_order) # Delete order if price is 0
        elif incoming_order.order_id not in self.order_ids:
            self._add_order(incoming_order) # Add order if it's new
        else:
            self._update_order(incoming_order) # Update order if it exists


    def _add_order(self, order):
        """Adds an order to the order book"""
        if order.side == Side.BUY:
            self.bids[order.price].append(order)
            self.order_ids[order.order_id] = order.price
        else:
            self.offers[order.price].append(order)
            self.order_ids[order.order_id] = order.price

    def _delete_order(self, order):
        """Removes an order from the order book"""
        if order.side == Side.BUY:
            self.bids[self.order_ids[order.order_id]] = [o for o in self.bids[self.order_ids[order.order_id]] if o.order_id != order.order_id]
        else:
            self.offers[self.order_ids[order.order_id]] = [
                o for o in self.offers[self.order_ids[order.order_id]] if o.order_id != order.order_id]

    def _update_order(self, order):
        """Updates an order in the order book"""
        self._delete_order(order)
        self._add_order(order)

    def best_bid(self):
        """Returns the best price of the buy side"""
        if self.bids:
            return max(self.bids.keys())
        else:
            return 0.

    def best_ask(self):
        """Returns the best price of the sell side"""
        if self.offers:
            return min(self.offers.keys())
        else:
            return float('inf')

    def spread(self):
        """Returns the spread"""
        return self.best_ask() - self.best_bid()


def log_orderbook_state_l3(orderbook: OrderBook):
    logger.info("Logging order book state in L3 format:")
    for price, orders in orderbook.bids.items():
        for order in orders:
            logger.info(
                f"Price: {price}, Side: 'B', Size: {order.size}, Order ID: {order.order_id}")

    for price, orders in orderbook.offers.items():
        for order in orders:
            logger.info(
                f"Price: {price}, Side: 'S' , Size: {order.size}, Order ID: {order.order_id}")


def log_orderbook_state_l2(orderbook: OrderBook):
    logger.info("Logging order book state in L2 format:")
    logger.info("Buy side:")
    for price in sorted(orderbook.bids.keys(), reverse=True):
        total_size = sum(order.size for order in orderbook.bids[price])
        if total_size != 0:
            logger.info(f"Price: {price}, Total Size: {total_size}")

    logger.info("Sell side:")
    for price in sorted(orderbook.offers.keys()):
        total_size = sum(order.size for order in orderbook.offers[price])
        if total_size != 0:
            logger.info(f"Price: {price}, Total Size: {total_size}")


def main():
    def reconstruct_orderbook(data: DataFrame):
        book = OrderBook()

        for idx, order in enumerate(data.itertuples(index=False, name="OrderBookDelta")):
            book.apply_delta(order)

            logger.info(idx)

            logger.info(' log_orderbook_state_l2 '.center(80, "-"))
            log_orderbook_state_l2(book)

            logger.info(' log_orderbook_state_l3 '.center(80, "-"))
            log_orderbook_state_l3(book)

    data = read_csv("sample-data.csv.gz") # Read input data
    # Swap the 'px' and 'qty' columns to correct the inversion of prices and quantities in the data
    data['px2'] = data['qty']
    data['qty'] = data['px']
    data['px'] = data['px2']
    data.to_csv("sample-data-headed.csv", index=False) # Write modified data to a new file
    try:
        reconstruct_orderbook(data)
    except Exception as e:
        logger.exception(e, exc_info=True)
        raise SystemExit("An error occurred")

    sys.exit(0)


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print("Aborted!")