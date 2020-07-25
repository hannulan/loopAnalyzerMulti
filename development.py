#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 14:14:55 2020

@author: mattiasbrannstrom
"""

from io import StringIO
import json 
import numpy as np
import pandas as pd
import requests
#import maya


import datetime as dt
import Reader
import Analyzer

import help_func

# Setting for everyone:
timeCGMStableMin = 20; 


ef = 'entries_ex_caspian.json';
name = 'Daniel'
tf = 'treatments_ex_nightscoutcaspian.json'
startDate = dt.date(2020, 7, 6)
stopDate = dt.date(2020, 7, 6)
  

reader = Reader.Reader(name, ef, tf, timeCGMStableMin);
#reader.createCGMStructure();





#reader.createInsulinStructure();


# self.dfTreatments.columns
# Index(['_id', 'amount', 'created_at', 'eventType', 'duration', 'timestamp',
#        'enteredBy', 'rate', 'absolute', 'temp', 'utcOffset', 'carbs',
#        'insulin', 'programmed', 'type', 'unabsorbed', 'reason',
#        'insulinNeedsScaleFactor', 'remoteAddress', 'absorptionTime',
#        'foodType'],
#       dtype='object')

# self.dfTreatments.eventType.unique()
# array(['Temp Basal', 'Correction Bolus', 'Temporary Override',
#        'Sensor Start', 'Meal Bolus', 'Resume Pump', 'Suspend Pump', nan],
#       dtype=object)

# All bolus events: 'Correction Bolus' and 'Meal Bolus'