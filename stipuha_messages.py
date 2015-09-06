
# -*- coding: utf-8 -*-

import requests
import csv
import random
from decimal import Decimal
import decimal
from datetime import *

class StipuhaMessages:

    _rub_to_usd_rate = None
    _rate_timeout = timedelta(hours=24)
    _last_rate_request = datetime.now()

    FILE = "stipuha_prices.csv"

    stipuha_prices = None

    @staticmethod
    def get_rub_to_usd_rate():
        if StipuhaMessages._rub_to_usd_rate is None or \
           StipuhaMessages._last_rate_request + StipuhaMessages._rate_timeout < datetime.now():
            r = requests.get('https://currency-api.appspot.com/api/RUB/USD.json')
            StipuhaMessages._rub_to_usd_rate = float(r.json()['rate'])
        return StipuhaMessages._rub_to_usd_rate

    @staticmethod
    def generate_stipuha_message(stipuha):
        if isinstance(stipuha, (int, long)):
            if StipuhaMessages.stipuha_prices is None:
                StipuhaMessages.load_stipuha_prices()
            price = random.choice(StipuhaMessages.stipuha_prices)
            decimal.getcontext().prec=3
            stipuha_in_usd = Decimal(stipuha) * Decimal(StipuhaMessages.get_rub_to_usd_rate())
            price_in_stipuha = stipuha_in_usd / Decimal(price[1])
            return ("Твоя стипушка - {:.2f}$. Поздравляю!" +
                    "\n" + "На нее ты можешь купить {:20f} процента {}.")\
                .format(stipuha_in_usd, price_in_stipuha, price[0])


    @staticmethod
    def load_stipuha_prices():
        StipuhaMessages.stipuha_prices = []
        with open(StipuhaMessages.FILE, "r+") as csvfile:
            reader = csv.reader(csvfile, dialect=csv.excel_tab)
            for row in reader:
                StipuhaMessages.stipuha_prices.append(row)
