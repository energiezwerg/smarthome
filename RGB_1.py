# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 07:37:12 2019

@author: fische12

RGB - Wechsel
"""
import numpy as np
import random

def rgb_col():
    n =10
    col = np.zeros((2,3), dtype=np.int)
    for i in range(2):
        r_col = int(random.random()*256)
        g_col = int(random.random()*256)
        b_col = int(random.random()*256)
        col[i,:] = (r_col, g_col, b_col)
    # interpolation von Wert 1>2    
    r_inter = np.linspace(col[0,0],col[1,0],n, dtype=int)
    g_inter = np.linspace(col[0,1],col[1,1],n, dtype=int)
    b_inter = np.linspace(col[0,2],col[1,2],n, dtype=int)
#    return r_inter[0], g_inter[0], b_inter[0]
    for i in range(n):
        col = [r_inter[i],g_inter[i],b_inter[i]]
        time.sleep(.5)
        print(col)
        
 return rgb_col()