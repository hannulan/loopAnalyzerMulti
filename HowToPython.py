# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 09:10:20 2020

@author: hannu
"""


Kladd: 
    
..:: Pyhton Howto ::..
    Pandas dataframes: 
        
    # Hitta specifika rader (1:10) i specifik column, 'rate'
    reader.dfTreatments['rate'][1:10]
    
    # Hitta alla kolumner på en viss rad (18)
    reader.dfBolus.iloc[18]
    
    # Skapa en vektor med sant/falskt och sen använda den för tat plocka ut de index där vektorn är sant.
    self.idxToRemove = self.dfTreatments['timestamp'].isnull();
    self.dfTreatments = self.dfTreatments[~self.idxToRemove]; # Remove all rows with timestamp = nan
    # reseta indexen
    self.dfTreatments.reset_index(inplace = True)
            
    
    
    
    self.dfCGMNight = dfCGM.iloc[self.idxNight];
    idxNight = np.argwhere(idxNightTemp).flatten().tolist();
    
    np.sum(self.dfBolus['bolus'])      
          
    
    
    for rr in range(4,2):
        print('rr: ' + str(rr))
    
    
    def findIdxNightDay(self):
        ii = 0; 
        minutes  = [[] for i in range(len(self.dfCGM))]; 
        idxNightTemp = [0 for i in range(len(self.dfCGM))]; 
        idxDayTemp   = [0 for i in range(len(self.dfCGM))]; 
        idxDay2Temp  = [0 for i in range(len(self.dfCGM))]; 
        
        while ii < len(self.dfCGM):
            self.dfCGM['dateTime'][ii]    
            minutes[ii]  = self.dfCGM['dateTime'][ii].minute + self.dfCGM['dateTime'][ii].hour*60;
            if self.nightTimeMinute[0] < minutes[ii] & minutes[ii] < self.nightTimeMinute[1]: 
                idxNightTemp[ii] = 1
                idxDay2Temp[ii]   = 0
            else: 
                idxNightTemp[ii] = 0
                idxDay2Temp[ii]   = 1
            
            if self.dayTimeMinute[0] < minutes[ii] & minutes[ii] < self.dayTimeMinute[1]:
                idxDayTemp[ii]   = 1
            ii = ii + 1;
            
        idxNight = np.argwhere(idxNightTemp).flatten().tolist();
        idxDay   = np.argwhere(idxDayTemp).flatten().tolist();
        idxDay2  = np.argwhere(idxDay2Temp).flatten().tolist();
            
        return idxNight, idxDay, idxDay2   

