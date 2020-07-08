# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:13:05 2019

@author: hannulan
"""
"""

web api = api över http
rest api, ett web api med viss bestämd ordning. 

GET is generally used to get information about some object or record that already exists.
POST is typically used when you want to create something.

# Step one for every Python app that talks over the web
$ pip install requests



dfRes = help_func.decreaseDataStructureDateTime(akselReader.dfCGM, dateTime1, dateTime2)

#dfRes2 = help_func.decreaceDataStructureTime(akselReader.dfCGM, time1, time2)


dfCGM = akselReader.dfCGM ## Dessa är alltså samma datautrymme, så om jag tar bort den ena tar jag bort från den andra. 

targetValue = [4*18, 8*18];
rangeValue = [4*18,10*18];

#idx = (dfCGM['cgm'] >= targetValue[0]) & (dfCGM['cgm'] <= targetValue[1])


# Beärkna deltaTime
deltaTime = [];
entry = dfCGM['dateTime'][0];
for ii in range(0,len(dfCGM)-1): # range(0,len(dfCGM)):
    nextEntry = dfCGM['dateTime'][ii+1];
    deltaTime.append(entry - nextEntry);
    entry = nextEntry; 
    
    #deltaTime.append()
    
# Hitta alla deltaTime > 5.1 min och < 45
    


deltaSeconds = pd.Series([val.total_seconds() for val in deltaTime])
# Interpolera lite :)
counter = 0; 
for ii in deltaSeconds:
    #print('hej')
    #print(ii)
    #print(counter)
    if (ii > 5.1*60) & (ii < 20*60):
        # Beräkna räta linjen: 
        print(ii/60)
        print('interpolate')
        print(counter)
        
    counter = counter + 1; 
#idxDeltaTimeGood = deltaTime < 20; # Delta time måste vara mindre än 20 min
