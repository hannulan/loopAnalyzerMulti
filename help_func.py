# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:08:48 2019

@author: hannulan
"""

# File with help functions: 

import pandas as pd
import numpy as np

def sortDateTime(dtArray, dateTime1, dateTime2):
    # Find index for all times between dateTime1 and dateTime2, where dateTime1 is most recent
  
    dr1 = dtArray < dateTime1;
    dr2 = dtArray > dateTime2;
    res = dr1 & dr2; 
    return res

def sortTime(dtArray, time1, time2):
    # Find index for all times between time1 and time2, where time1 is most recent
    # Do not care about date
    
    temp = pd.Series([val.time() for val in dtArray])
    dr1 = temp < time1;
    dr2 = temp > time2;
    res = dr1 & dr2; 
    
    return res

def sortDate (dtArray, date1, date2):
    # Find index for all times between time1 and time2, where time1 is most recent
    # Do not care about time
    print('temp')
    
def decreaseDataStructureDateTime(dfIn, date1, date2):
    # This function find all index between date1 and date2, where date1 is most recent
    # And than creates new DataFrame with the same coloumns but only data with dates between those dates1. 
    idx = sortDateTime(dfIn['dateTime'], date1, date2);
    col = dfIn.columns;
    dfRes = pd.DataFrame(columns = col)
    print(dfRes)

    #for ii in col: 
     #   dfRes[ii] = np.array(dfIn[ii][idx]);
    
    return dfRes

def decreaseDataStructureTime(dfIn, time1, time2):
    # This function: 
    
    dfRes = pd.DataFrame(columns = col)
    
    col = dfIn.columns;
    for ii in col: 
        print(ii);
        #print(dfCGM[ii]);
        dfRes[ii] = np.array(dfIn[ii][idx]);
        #dfInsulin['bolus'] = np.array(dfTreatments['insulin'][idx]);
   
    
    return dfRes