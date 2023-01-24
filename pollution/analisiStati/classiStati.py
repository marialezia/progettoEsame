import numpy as np
import pandas as pd
import sys, os
from scipy import constants, fft
from tqdm import tqdm


class Stato2:

    def __init__(self):
        self.date = np.empty(0)
        self.siteNum = np.empty(0)
        self.address = np.empty(0)
        self.no2 = np.empty(0)
        self.o3 = np.empty(0)
        self.so2 = np.empty(0)
        self.co = np.empty(0)
        
    def aggiornaStato(self, date, sNum, address, no2, o3, so2, co):
        self.date = date
        self.siteNum = sNum
        self.address = address
        self.no2 = no2
        self.o3 = o3
        self.so2 = so2
        self.co = co

    def sintesi(self, statoFft):
        self.date = statoFft.date
        self.siteNum = statoFft.siteNum
        self.address = statoFft.address
        self.no2 =  fft.irfft(statoFft.no2Fft, len(self.date))
        self.o3 =  fft.irfft(statoFft.o3Fft, len(self.date))
        self.so2 =  fft.irfft(statoFft.so2Fft, len(self.date))
        self.co =  fft.irfft(statoFft.coFft, len(self.date))
        

        
class Stato2Fft:

    def __init__(self, stato):
        self.date = stato.date
        self.siteNum = stato.siteNum
        self.address = stato.address
        self.no2Fft = fft.rfft(stato.no2)
        self.o3Fft = fft.rfft(stato.o3)
        self.so2Fft = fft.rfft(stato.so2)
        self.coFft = fft.rfft(stato.co)
        self.no2F = 0.5*fft.rfftfreq(len(stato.no2))
        self.o3F = 0.5*fft.rfftfreq(len(stato.o3))
        self.so2F = 0.5*fft.rfftfreq(len(stato.so2))
        self.coF = 0.5*fft.rfftfreq(len(stato.co))
        self.no2P = np.absolute(self.no2Fft)**2
        self.o3P = np.absolute(self.o3Fft)**2
        self.so2P = np.absolute(self.so2Fft)**2
        self.coP = np.absolute(self.coFft)**2

    def mascheraStato(self, maskNo2, maskO3, maskSo2, maskCo):
        self.no2Fft[maskNo2]=0
        self.o3Fft[maskO3]=0
        self.so2Fft[maskSo2]=0
        self.coFft[maskCo]=0
        self.no2P = np.absolute(self.no2Fft)**2
        self.o3P = np.absolute(self.o3Fft)**2
        self.so2P = np.absolute(self.so2Fft)**2
        self.coP = np.absolute(self.coFft)**2


    

        

        

