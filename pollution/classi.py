import numpy as np
import pandas as pd
import sys, os
import funzioni as fz
from scipy import constants, fft
from tqdm import tqdm

"""
Nel seguente script sono definite le classi: 
- Stato2: per l'analisi degli stati, ha informazioni su date di campionamento, concentrazioni inquinanti
- Stato2Fft: per l'analisi degli stati, ha informazioni su date, frequenze, coefficienti di fourier e potenze
- Site: per l'analisi delle stazioni, rappresenta una stazione di monitoraggio, ha informazioni su date di campionamento, concentrazioni inquinanti
- SiteFft:per l'analisi delle stazioni, ha informazioni su date, frequenze, coefficienti di fourier e potenze della stazione di monitoraggio
- Stato: per l'analisi delle stazioni, ha informazioni sulle stazioni di monitoraggio di quello stato e rispettivo numero
- StatoFft: per l'analisi delle stazioni, ha informazioni sulle stazioni di monitoraggio di tipo fft e rispettivo numero
"""
#---------------------------------------------------------------#
#           Definizioni classi per Analisi Stati                #
#---------------------------------------------------------------#

class Stato2:
    '''
la classe Stato2 ha 5 attributi: i giorni in cui sono registrati i dati (date) e la concentrazione di inquinanti (no2, o3, so2, co).
Ha 3 metodi: 
__init__: crea gli attributi come array vuoti
aggiornaStato: aggiorna gli attributi con quelli inseriti
sintesi: risintetizza le trasformate
'''

    def __init__(self):
        self.date = np.empty(0)
        self.days = np.empty(0)
        self.no2 = np.empty(0)
        self.o3 = np.empty(0)
        self.so2 = np.empty(0)
        self.co = np.empty(0)
        
    def aggiornaStato(self, date, no2, o3, so2, co):
        self.date = date
        self.days = np.arange(0, len(self.date))
        self.no2 = no2
        self.o3 = o3
        self.so2 = so2
        self.co = co

    def sintesi(self, statoFft):
        self.date = statoFft.date
        self.days = statoFft.days
        self.no2 =  fft.irfft(statoFft.no2Fft, len(self.date))
        self.o3 =  fft.irfft(statoFft.o3Fft, len(self.date))
        self.so2 =  fft.irfft(statoFft.so2Fft, len(self.date))
        self.co =  fft.irfft(statoFft.coFft, len(self.date))
        

        
class Stato2Fft:
    ''' attributi: date, fft degli inquinanti, frequenze degli inquinanti, potenza degli inquinanti
metodi: 
__init__: aggiorna attributi calcolandoli da quelli dello stato inseriti
mascheraStato: filtra coefficienti mettendoli a zero a secondo le maschere inserite
'''

    def __init__(self, stato):
        self.date = stato.date
        self.days = stato.days
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


#---------------------------------------------------------------#
#           Definizioni classi per Analisi Stazioni                #
#---------------------------------------------------------------#    

class Site:
    '''
attributi: i giorni in cui sono registrati i dati (date) e la concentrazione di inquinanti (no2, o3, so2, co), numero di stazione (sNUm), indirizzo e città (address e city).
Ha 3 metodi: 
__init__: crea gli attributi come array vuoti
aggiornaStato: aggiorna gli attributi con quelli inseriti
sintesi: risintetizza le trasformate
'''
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
	'''	
	attributi: elenco stazioni (sites) e numero stazioni (siteNUm)
	metodi: 
	__init__: crea elenco vuoto di stazioni, inserisce numero stazioni
	addSite: aggiunge stazione a sites
	copiaStato: fa una copia dello stato passato come parametro
	sintesi: sintetizza statoFFt
	'''

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
''' attributi: date, sNum, address, city della stazione, trasformata degli inquinanti, frequenze degli inquinanti, potenza degli inquinanti
metodi: 
__init__: aggiorna attributi calcolandoli da quelli della stazione inseriti
mascheraSite: filtra coefficienti mettendoli a zero a secondo le maschere inserite
'''
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
"""
attributi: elenco sitesFft e dei numeri corrispondenti (siteNumFFt)
metodi: 
__init__: crea attributi vuoti
addSites: aggiunge elenco di sitesFft da uno stato passato come parametro
mascheraStato: filtra coefficienti di ogni siteFft 

"""
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
         

        

