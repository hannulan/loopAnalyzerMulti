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
fn = 'temp_medtronic_short.csv';


fn01 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic01/data01_ES.csv'
reader01 = ReaderMedtronic.ReaderMedtronic('ES01', fn01)
analyzer01 = Analyzer.Analyzer('ES01', reader01)
analyzer01.printAll()

fn02 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic02/AO 2021-02-15.csv'
reader02 = ReaderMedtronic.ReaderMedtronic('AO02', fn02)
analyzer02 = Analyzer.Analyzer('AO02', reader02)
analyzer02.printAll()


fn03 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic03/K I 2021-02-16.csv'

fn04 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic04/OH 2021-02-15.csv'
fn05 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic05/OE 2021-02-16.csv'

fn06 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic06/LS 2021-02-22.csv'
fn07 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic07/CS 2021-02-23.csv'

fn08 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic08/NM medtronic 8 2021-02-25.csv'
fn09 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic09/KB 21-02-25.csv'

fn10 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic10/FS 2021-03-02.csv'
fn11 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic11/I B 2021-03-02.csv'

fn12 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic12/MB 2021-03-22.csv'
fn13 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic13/SA 2021-03-22.csv'

fn14 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic14/EJ 2021-04-13.csv'
fn15 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic15/EE 2021-04-16.csv'

#fn16 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic16/.csv'
fn17 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic17/OS 2021-04-21.csv'

#fn18 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic18/.csv'
#fn19 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic19/.csv'
#fn20 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic20/.csv'
#fn21 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic21/.csv'
#fn22 = 'C:/Users/hannu/Dropbox/Diassist_OpenAPS_study/Data_fran_deltagare/Medtronic/Medtronic22/.csv'

fnList = list()
fnList = [fn01, fn02, fn03, fn04, fn05, fn05, fn06, fn07, fn08, fn09, fn10, fn11, fn12, fn13, fn14, fn15, fn17]
nameList = ['p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07', 'p08', 'p09', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p17']
nList = [2, 3];

analyzerList = list();

for nn in nList:
    fn = fnList[nn]
    reader   = ReaderMedtronic.ReaderMedtronic(nameList[nn], fn)
    analyzer = Analyzer.Analyzer(nameList[nn], reader)
    analyzer.printAll()
    analyzerList.append(analyzer)


reader   = ReaderMedtronic.ReaderMedtronic(nameList[nn], fn)
analyzer = Analyzer.Analyzer(nameList[nn], reader)

# readerTest = ReaderMedtronic.ReaderMedtronic('Test', dfCGM, dfInsulin)
readerTest = ReaderMedtronic.ReaderMedtronic('Test', fn)

analyzerTest = Analyzer.Analyzer('Test', readerTest)

analyzerTest.writeAll()   

