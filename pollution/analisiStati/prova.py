import numpy as np
import pandas as pd
import sys, os
import classiStati as clSt
import funzioniStati as fzSt
import matplotlib.pyplot as plt
import graficiStati as grSt
from scipy import constants, fft

kaDf = pd.read_csv('~/progettoEsame/fileCSV/newKansas.csv')
no2 = kaDf['no2'].values
print(no2)
days = pd.to_datetime(kaDf['Date Local'], format = '%d/%m/%Y').values
print(days)

#plt.plot(days, no2)
#plt.show()

no2fft = fft.rfft(no2)
no2F = 0.5*fft.rfftfreq(len(no2))
no2P = np.absolute(no2fft)**2
'''print(no2fft)
print(no2F)
print(no2P)
plt.plot(no2F[1:no2fft.size//2], no2P[1:no2fft.size//2])
plt.show()
'''
print(len(no2))
print(len(no2fft))
#print(no2P)
maxno2 = np.argmax(no2P[1:])
print(maxno2)
maskMassimo = no2fft != no2fft[maxno2+1]

no2fftFiltroMassimo = no2fft.copy()
no2fftFiltroMassimo[maskMassimo] = 0
#print(no2fftFiltro)
mask1no2= no2F > 0.05
no2fftFiltro1 = no2fft.copy()
no2fftFiltro1[mask1no2] = 0
mask2no2= no2F > 0.2
no2fftFiltro2 = no2fft.copy()
no2fftFiltro2[mask2no2] = 0

plt.plot(no2F, no2fft, alpha = 0.8, label = 'originale')
plt.plot(no2F, no2fftFiltroMassimo, alpha = 0.8, label = 'massimo')
plt.plot(no2F, no2fftFiltro1, alpha = 0.8, label = 'filtro1')
plt.plot(no2F, no2fftFiltro2, alpha = 0.8, label = 'filtro2')
plt.legend()
plt.show()

no2SintesiMassimo = fft.irfft(no2fftFiltroMassimo)
no2Sintesi1 = fft.irfft(no2fftFiltro1)
no2Sintesi2 = fft.irfft(no2fftFiltro2)
plt.plot(days, no2, alpha = 0.8, label = 'originale')
plt.plot(days, no2Sintesi2, alpha = 0.8, label = 'filtro2')
plt.plot(days, no2Sintesi1, alpha = 0.8, label = 'filtro1')
plt.plot(days, no2SintesiMassimo, alpha = 0.8, label = 'massimo')
plt.legend()
plt.show()


plt.plot(days, no2, label = 'originale')
plt.plot(days, no2Sintesi1,  label = 'filtro1')
plt.legend()
plt.show()
