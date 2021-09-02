# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:13:16 2021

@author: hannu
"""
from io import StringIO
import json 
import numpy as np
import pandas as pd
import requests
#import maya

import csv 
import datetime as dt

import Reader
import Analyzer
import ReaderMedtronic

pd.set_option('mode.chained_assignment', None)

fn = 'temp_medtronic.csv';

# readerTest = ReaderMedtronic.ReaderMedtronic('Test', dfCGM, dfInsulin)
readerTest = ReaderMedtronic.ReaderMedtronic('Test', fn)

analyserTest = Analyzer.Analyzer('Test', readerTest)

analyserTest.writeAll()   