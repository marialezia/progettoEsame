import numpy as np
import pandas as pd
import sys, os
from scipy import constants, fft
from tqdm import tqdm

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
    def __init__(self, siteNum):
        self.sites = np.empty(0)
        self.siteNum = siteNum

    def addSite(self, site):
        self.sites = np.append(self.sites, site)
        
class SiteFft:
    def __init__(self, site):
        self.date = site.date
        self.cCode = site.cCode
        self.sNum = site.sNum
        self.no2Fft = fft.fftshift(fft.fft(site.no2))
        self.no2F = fft.fftshift(fft.fftfreq(len(site.no2)))
        self.o3Fft = fft.fftshift(fft.fft(site.o3))
        self.o3F = fft.fftshift(fft.fftfreq(len(site.o3)))
        self.so2Fft = fft.fftshift(fft.fft(site.so2))
        self.so2F = fft.fftshift(fft.fftfreq(len(site.so2)))
        self.coFft = fft.fftshift(fft.fft(site.co))
        self.coF = fft.fftshift(fft.fftfreq(len(site.co)))
        self.no2P = np.absolute(self.no2Fft)**2
        self.o3P = np.absolute(self.o3Fft)**2
        self.so2P = np.absolute(self.so2Fft)**2
        self.coP = np.absolute(self.coFft)**2
        

        
class StatoFft:
    def __init__(self):
        self.sitesFft = np.empty(0)
        self.siteNumFft = 0
        
    def addSites(self, stato):
        for i in tqdm(stato.sites, 'creating statoFft: '):
            self.sitesFft = np.append(self.sitesFft, SiteFft(i))
        self.siteNumFft = stato.siteNum


