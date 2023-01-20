import numpy as np
import pandas as pd
import sys, os




class Site:      
    def __init__(self, date, sCode, cCode, sNum, address, state, country, city, no2, no2Err, o3, o3Err, so2, so2Err, co, coErr):
        self.date = date
        self.sCode = sCode
        self.cCode = cCode
        self.sNum = sNum
        self.address = address
        self.state = state
        self.country = country
        self.city = city
        self.no2 = no2
        self.no2Err = no2Err
        self.o3 = o3
        self.o3Err = o3Err
        self.so2 = so2
        self.so2Err = so2Err
        self.co = co
        self.coErr = coErr

class Stato:
    def __init__(self):
        self.sites = np.empty(0)
    def addSite(self, site):
        self.sites = np.append(self.sites, site)
        
        
        
