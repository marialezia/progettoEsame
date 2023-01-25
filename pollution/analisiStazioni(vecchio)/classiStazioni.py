import numpy as np
import pandas as pd
import sys, os
from scipy import constants, fft
from tqdm import tqdm
import funzioniStazioni as fz

class Site:
    def __init__(self):
        self.date = np.empty(0)
        self.sNum = np.empty(0)
        self.address = np.empty(0)
        self.city = np.empty(0)
        self.no2 = np.empty(0)
        self.o3 = np.empty(0)
        self.so2 = np.empty(0)
        self.co = np.empty(0)
        
    def aggiornaSite(self, date, sNum, address, city, no2, o3, so2, co):
        self.date = date
        self.sNum = sNum
        self.address = address
        self.city = city
        self.no2 = no2
        self.o3 = o3
        self.so2 = so2
        self.co = co

    def sintesi(self, siteFft):
        self.date = siteFft.date
        self.sNum = siteFft.sNum
        self.address = siteFft.address
        self.city = siteFft.city
        self.no2 =  fft.irfft(siteFft.no2Fft, len(self.date))
        self.o3 =  fft.irfft(siteFft.o3Fft, len(self.date))
        self.so2 =  fft.irfft(siteFft.so2Fft, len(self.date))
        self.co =  fft.irfft(siteFft.coFft, len(self.date))

class Stato:
    def __init__(self, siteNum):
        self.sites = np.empty(0)
        self.siteNum = siteNum

    def addSite(self, site):
        self.sites = np.append(self.sites, site)

    def copiaStato(self, stato):
        self.siteNum = stato.siteNum
        self.sites = stato.sites
        
    def sintesi(self, statoFft):
        for i in range(len(statoFft.sitesFft)):
            self.sites = np.append(self.sites, fz.sintesiSite(statoFft.sitesFft[i]))

        
class SiteFft:
    def __init__(self, site):
        self.date = site.date
        self.sNum = site.sNum
        self.address = site.address
        self.city = site.city
        self.no2Fft = fft.rfft(site.no2)
        self.o3Fft = fft.rfft(site.o3)
        self.so2Fft = fft.rfft(site.so2)
        self.coFft = fft.rfft(site.co)
        self.no2F = 0.5*fft.rfftfreq(len(site.date))
        self.o3F = 0.5*fft.rfftfreq(len(site.date))
        self.so2F = 0.5*fft.rfftfreq(len(site.date))
        self.coF = 0.5*fft.rfftfreq(len(site.date))
        self.no2P = np.absolute(self.no2Fft)**2
        self.o3P = np.absolute(self.o3Fft)**2
        self.so2P = np.absolute(self.so2Fft)**2
        self.coP = np.absolute(self.coFft)**2

    def mascheraSite(self, maskNo2, maskO3, maskSo2, maskCo):
        self.no2Fft[maskNo2]=0
        self.o3Fft[maskO3]=0
        self.so2Fft[maskSo2]=0
        self.coFft[maskCo]=0
        self.no2P = np.absolute(self.no2Fft)**2
        self.o3P = np.absolute(self.o3Fft)**2
        self.so2P = np.absolute(self.so2Fft)**2
        self.coP = np.absolute(self.coFft)**2

class StatoFft:
    def __init__(self):
        self.sitesFft = np.empty(0)
        self.siteNumFft = np.empty(0)
        
    def addSites(self, stato):
        for i in stato.sites:
            self.sitesFft = np.append(self.sitesFft, SiteFft(i))
        self.siteNumFft = stato.siteNum

    def mascheraStato(self, maskNo2arr, maskO3arr, maskSo2arr, maskCoarr):
        for i in range(len(self.sitesFft)):
            self.sitesFft[i].mascheraSite(maskNo2arr[i], maskO3arr[i], maskSo2arr[i], maskCoarr[i])
 
