import numpy as np
import pandas as pd
import sys, os
import classiStazioni as clSz
import funzioniStazioni as fzSz
import matplotlib.pyplot as plt
import graficiStazioni as grSz

caDf = pd.read_csv('~/progettoEsame/fileCSV/newCalifornia.csv')

sitesNum = ([2,2004])
#creo lo stato in cui sono presenti la sottocategoria siteNum che corrisponde alle stazioni di monitoraggio, ogni stazione di monitoraggio ha i suoi dati sugli inquinanti distinti. faccio grafico degli inquinanti in funzione del tempo per ogni stazione di riferimento sia in grafici distinti (sublots) che nello stesso (plot)

california = fzSz.createStato(caDf, sitesNum)
#grSz.subplots(california)
#grSz.plot(california)

#calcolo trasformata di fourier degli inuinanti per ogni stazione di monitoraggio e faccio grafico spettro di potenza in funzione del tempo 

californiaFft = fzSz.createStatoFft(california)
#print(californiaFft.sitesFft[0].no2F)
#print(californiaFft.sitesFft[0].no2Fft)
#print(californiaFft.sitesFft[0].no2P)

grSz.subplotsFft(californiaFft)
grSz.subplotStazioni(california, 'california')

