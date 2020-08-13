# coding=utf-8
import logging
import sqlite3
from celery import Celery

logger = logging.getLogger(__name__)
app = Celery('hello', broker='amqp://guest@localhost//')


class dbORDERS(object):
    """
    Add and delete data from an in memory database.
    Celery using for async tasks
    """

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self._createOrderTable()

    def _createOrderTable(self):
        """
        Create table to hold orders
        """
        self.conn.execute('''CREATE TABLE ORDERS
        (timestamp TEXT    NOT NULL,
        orderId    TEXT    NOT NULL,
        ticker TEXT,
        side    TEXT,
        price   REAL,
        quantity    INTEGER);''')
        logging.info("Created table ORDER")

    def addData(self, Order):
        """
        Adding Order to table ORDERS
        """
        self.conn.execute('''INSERT INTO ORDERS VALUES (?,?,?,?,?,?);''',
                          (Order.timestamp, Order.orderId, Order.ticker, Order.side,
                           Order.price, Order.quantity))
        logging.info("Order inserted.")

    def deleteData(self, Order):
        """
        Cancel Order to table ORDERS
        """
        self.conn.execute('''DELETE FROM ORDERS WHERE orderId = ?;''', (Order.orderId,))
        logging.info("Order inserted.")


@app.task
def addOrder(db, data):
    """
    Public function to add order to TABLE ORDERS.
    """
    db.addData(data)


@app.task
def cancelOrder(db, data):
    """
    Public function to add order to TABLE ORDERS.
    """
    db.deleteData(data)

    # def getBestBidAndAsk(db, ticker):
    """
   TODO: Query to fetch and return min bid and max ask from database.
    """
# ob.db.conn.execute('''SELECT IFNULL(MIN(price), 0.0) || '/' ||   IFNULL(MAX(price), 0.0) FROM ORDERS WHERE ticker=
# ? GROUP BY ticker''', ('AAPL',)).fetchall()
