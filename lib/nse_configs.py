#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 22:00:39 2017

@author: raghuramkowdeed
"""

from nsepy import get_history, get_index_pe_history
import numpy as np
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta, TH


def is_nse_holiday(dt = date(2017,1,1)):
    #only add holidays that are expiry dates
    list_of_expiry_holidays = []
    list_of_expiry_holidays.append(date(2017,1,26))
    list_of_expiry_holidays.append(date(2016,3,24))
    list_of_expiry_holidays.append(date(2015,10,22))
    ## keep adding it to the list
    
    flag = dt in list_of_expiry_holidays
    return flag
    
    
def get_nse_expiry_date(dt = date(2017,1,1)):
    end_of_month = dt + relativedelta(day=31) 
    last_thrusday = end_of_month + relativedelta(weekday=TH(-1))

    is_holiday = is_nse_holiday(last_thrusday)
    expiry_date = last_thrusday
    
    if is_holiday :
        expiry_date = last_thrusday + relativedelta(days = -1)

    return expiry_date    

def is_index(underlying):
    index_list = []
    index_list.append('NIFTY')
    index_list.append('BANK_NIFTY')
    
    return underlying in index_list

def strike_width(underlying):
    d = {}
    d['NIFTY'] = 50
    
    return d[underlying]

def nearest_strike( f = 8000.5, strike_width= 50, strike_offset = 100):
    int_k = int(f/strike_width) *strike_width
    k = int_k + strike_offset
    return k 
    
