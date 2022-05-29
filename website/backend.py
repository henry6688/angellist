"""
Back end calculator
"""
from datetime import datetime, timedelta, time, date
from dateutil import parser
from abc import ABC, abstractmethod
import numpy as np
import os
import pandas as pd
import sys, inspect
import functools
import xarray as xr
import seaborn as sns
import logging


class Prorator(object):
    def __init__(self, input_data: dict):
        self.input_data = input_data

    def calculate(self) -> dict:
        allocation_amount = self.input_data['allocation_amount']
        investor_amounts = self.input_data['investor_amounts']

        # simple case: more than enough for every investor
        if sum([x['requested_amount'] for x in investor_amounts]) <= allocation_amount:
            return {x['name']: x['requested_amount'] for x in investor_amounts}

        # more complicated case: where we have to divide the pie among 'some' investors
        total_amount = sum([x['average_amount'] for x in investor_amounts])
        remain_allocation = allocation_amount
        result = dict()
        aggresive_investor = []     # store all investors who requested more than allowed

        for x in investor_amounts:
            allowed_amount = allocation_amount * x['average_amount'] / total_amount     # percentage that this investor is allowed to invest
            if x['requested_amount'] <= allowed_amount:     # this investor is not using up the quota, so give the full requested amount
                result[x['name']] = x['requested_amount']
                remain_allocation -= x['requested_amount']
            else:       # investor asking more than they are allowed
                aggresive_investor.append(x)

        # now divide the remaining pie among aggressive investors
        total_amount = sum([x['average_amount'] for x in aggresive_investor])
        for x in aggresive_investor:
            result[x['name']] = remain_allocation * x['average_amount'] / total_amount

        assert (allocation_amount == sum(result.values()))
        return result


if __name__ == "__main__":
    data = {
      "allocation_amount": 100,
      "investor_amounts": [
        {
          "name": "Investor A",
          "requested_amount": 100,
          "average_amount": 100
        },
        {
          "name": "Investor B",
          "requested_amount": 25,
          "average_amount": 25
        }
      ]
    }

    obj = Prorator(data)
    obj.calculate()
    print('Done!')
