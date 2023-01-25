import numpy as np
import pandas as pd
import sys, os
import classiStazioni as clSz
import funzioniStazioni as fzSz
import matplotlib.pyplot as plt
import graficiStazioni as grSz

ilDf = pd.read_csv('~/progettoEsame/fileCSV/newIllinois.csv')
sitesNum =([10,4002,4201])


#creo lo stato in cui sono presenti la sottocategoria siteNum che corrisponde alle stazioni di monitoraggio, ogni stazione di monitoraggio ha i suoi dati sugli inquinanti distinti. faccio grafico degli inquinanti in funzione del tempo per ogni stazione di riferimento sia in grafici distinti (sublots) che nello stesso (plot)


illinois = fzSz.createStato(ilDf, sitesNum)
grSz.subplots(illinois)



#calcolo trasformata di fourier degli inuinanti per ogni stazione di monitoraggio e faccio grafico spettro di potenza in funzione del tempo 

illinoisFft = fzSz.createStatoFft(illinois)
fzSz.subplotsFft(illinoisFft)
