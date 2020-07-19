# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:54:16 2020

@author: hannu
"""


" Testa basal och bolus strukturerna "

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



ef = 'entries_ex_caspian.json';
name = 'Daniel'
tf = 'treatments_ex_nightscoutcaspian.json'

reader  = Reader.Reader(name, ef, tf);

analyzer = Analyzer.Analyzer(name, reader.numDayNight, reader.dfCGM, reader.dfInsulin); 
analyzer.calcAllCGM(); 

analyzer.calcAllInsulin(); 

analyzer.writeAll();


# TODO: Double check if dfBolus also includes the micro boluses