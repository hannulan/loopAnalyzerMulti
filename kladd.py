# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 16:32:30 2019

@author: hannulan
"""

# Data types: 
"""
  dataStructMerge = struct;
  dataStructMerge.date             = {}; #repmat('YYYY-MM-DD', N, 1);
  dataStructMerge.time             = {}; #repmat('HH:MM', N, 1);
  dataStructMerge.timeEnd  = {}; #repmat('HH:MM', N, 1);
  dataStructMerge.dateTime         = '';
  dataStructMerge.bolus            = zeros(N,1);
  dataStructMerge.cgm              = zeros(N,1);
  dataStructMerge.bolusextended    = zeros(N,1);
  dataStructMerge.bs               = zeros(N,1); % z = S.bsB - S.
  dataStructMerge.kh               = zeros(N,1); 
  dataStructMerge.motionLevel     = zeros(N,1);
  dataStructMerge.dataType         = zeros(N,1); 
  dataStructMerge.selectedDataType = zeros(N,1);  
  """
  
  """
  date
  time
  timeEnd
  dateTime
  bolus
  bolusExtended
  bolusExtPercentage
  bolusExtTime
  cgm   
  bs
  carb
  basalRate
"""
  
  """
  Treatments: 
      ['_id', 'absolute', 'absorptionTime', 'carbs', 'created_at', 'duration',
       'enteredBy', 'eventType', 'insulin', 'programmed', 'rate', 'temp',
       'timestamp', 'type', 'unabsorbed'],
  
  Response
     ['date', 'dateString', 'device', 'direction', 'sgv', 'trend',
       'type'],
     
  """
  
  
  
  
  