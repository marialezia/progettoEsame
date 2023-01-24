import numpy as np
import pandas as pd
import sys, os
import classiStazioni as clSz
import funzioniStazioni as fzSz
import matplotlib.pyplot as plt
import graficiStazioni as grSz

kaDf = pd.read_csv('~/progettoEsame/fileCSV/newKansas.csv')
sitesNum =([2, 21])

#creo lo stato in cui sono presenti la sottocategoria siteNum che corrisponde alle stazioni di monitoraggio, ogni stazione di monitoraggio ha i suoi dati sugli inquinanti distinti. faccio grafico degli inquinanti in funzione del tempo per ogni stazione di riferimento sia in grafici distinti (sublots) che nello stesso (plot)

kansas = fzSz.createStato(kaDf, sitesNum)
#grSz.subplots(kansas)
#grSz.plot(kansas)

#calcolo trasformata di fourier degli inuinanti per ogni stazione di monitoraggio e faccio grafico spettro di potenza in funzione del tempo 

kansasFft = fzSz.createStatoFft(kansas)
#print(kansasFft.sitesFft[0].no2F)
#print(kansasFft.sitesFft[0].no2Fft)
#print(kansasFft.sitesFft[0].no2P)

grSz.subplotsFft(kansasFft)
grSz.subplotStazioni(kansas, 'kansas')
