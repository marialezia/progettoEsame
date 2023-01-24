import numpy as np
import pandas as pd
import sys, os
import classiStati as clSt
import funzioniStati as fzSt
import matplotlib.pyplot as plt
import graficiStati as grSt

ilDf = pd.read_csv('~/progettoEsame/fileCSV/newIllinois.csv')
sitesNum =([10,4002,4201])

#creo stato illinois (tutte le stazioni insieme) e faccio il plot delle concentrazioni dei vari inquinanti in funzione del tempo
illinois2 = fzSt.createStato2(ilDf)
grSt.plotInquinanti2(illinois2)

#calcolo le trasformate di fourier dei vari inquinanti e faccio il plot dello spettro di potenza (modulo quadro dei coefficienti) in funzione delle frequenze
illinoisFft2 = clSt.Stato2Fft(illinois2)
grSt.plotFft2(illinoisFft2)





