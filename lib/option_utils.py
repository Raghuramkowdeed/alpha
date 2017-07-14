
import vollib.black.implied_volatility as ivlib
import vollib.black as bs
import vollib.black.greeks.analytical as greekslib
import pandas as pd
import numpy as np 

import datetime as dt

def iv(p,f,k,t,r = 6.25/100,op_type='c'):
    vol = ivlib.implied_volatility_of_discounted_option_price(p,f,k,r,t,op_type)
    return vol

def op(f,k,vol,t,r = 6.25/100, op_type ='c'):
    if op_type == 'c':
        return bs.black_call(f,k,t,r,vol)
    else:
        return bs.black_put(f,k,t,r,vol)
    
def get_expiry_date(y=2017,m=01):
    # yet to finish
    return 0    

def get_ttm(expiry_str = "20170628"):
    curr_date = dt.date.today()
    #curr_date = curr_date.date()
    d2 = dt.datetime.strptime(expiry_str, "%Y%m%d")
    d2 = d2.date()
    td = d2 - curr_date
    ttm = float(td.days)/365
    return ttm
    # need to account for holidays , intra day time calculations
    
def get_target_price(pc_f,curr_f, curr_op, k,t,op_type='c', r = 6.25/100):
    vol = iv(curr_op,curr_f,k,t,r,op_type)
    t_f = curr_f*(1+(pc_f/100))
    t_op = op(t_f,k,vol,t,r,op_type)
    return t_op

def delta(p,f,k,t,r=6.25/100,op_type ='c', step = 1.0):
    vol = iv(p,f,k,t,r,op_type)
    target_f = f*(1+  (step/100) ) 
    
    p1 = op( f,k,vol,t,r,op_type )
    p2 = op( target_f,k,vol,t,r,op_type )
    val = p2 - p1

    return val

def vega(p,f,k,t,r=6.25/100,op_type ='c', step = 1.0):
    vol = iv(p,f,k,t,r,op_type)
    target_vol = vol * (1 + (step/100))
    
    p1 = op( f,k,vol,t,r,op_type )
    p2 = op( f,k,target_vol,t,r,op_type )
    return p2 -p1

def theta(p,f,k,t,r=6.25/100,op_type ='c', step = 1.0/365):
    vol = iv(p,f,k,t,r,op_type)
    target_t = t - step
    
    p1 = op(f,k,vol,t,r,op_type)
    p2 = op(f,k,vol,target_t,r,op_type)
    return p2 - p1

def gamma(p,f,k,t,r=6.25/100,op_type ='c', step = 1.0):
    vol = iv(p,f,k,t,r,op_type)
    target_f = f*(1+  (step/100) ) 
    
    p1 = op( f,k,vol,t,r,op_type )
    p2 = op( target_f,k,vol,t,r,op_type )
    d = greekslib.delta( flag = op_type,F=f,K=k, r=r, t=t, sigma = vol)
    val = p2 - p1 - d*(target_f - f)
    return val



def greeks(p,f,k,t,r=6.25/100,op_type ='c', f_step = 1.0, vol_step=1.0, t_step = 1.0/365):
    d = delta(p,f,k,t,r,op_type, f_step )
    v = vega(p,f,k,t,r,op_type, vol_step )
    decay = theta(p,f,k,t,r,op_type, t_step )
    gm = gamma(p,f,k,t,r,op_type, f_step )
    
    dic = {'delta':d, 'vega':v, 'theta': decay, 'gamma': gm}
    return dic

def build_prices_dic(op_type, f, strikes, prices, ttm, r):
    dic = {}
    
    for i,k in enumerate(strikes):
        temp_dic = {'p':prices[i], 'f':f, 'k':k,'t':ttm, 'r':r, 'op_type':op_type }
        dic[k] = temp_dic        
    return dic    

def get_vol_curve(prices_dic):
    
    strikes = []
    vols = []
    for k, op_arg in prices_dic.items():
        strikes.append(k)
        v = iv(**op_arg)
        vols.append(v)
    data = pd.DataFrame({'strike':strikes, 'vol':vols})
    
    return data