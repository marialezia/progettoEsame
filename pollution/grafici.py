import pandas as pd
import numpy as np
import classi as cl
import sys, os
from tqdm import tqdm
import matplotlib.pyplot as plt


#---------------------------------------------------------------#
#       Definizione moduli grafici per analisi Stati            #
#---------------------------------------------------------------#

def plotInquinanti2(stato, title):
    plt.figure(figsize = (12,12))
    plt.title(title)
    plt.plot(stato.date, stato.no2,label= 'NO2')
    plt.plot(stato.date, stato.o3, label = 'O3')
    plt.plot(stato.date, stato.so2, label = 'SO2')
    plt.plot(stato.date, stato.co,  label = 'CO')
    plt.grid()
    plt.xlabel('Time', size = 10)
    plt.ylabel('concentrazione')
    plt.legend()
    plt.show()


def plotFft2(stato, title):
    lNo2 = len(stato.no2F)//2
    lO3 = len(stato.o3F)//2
    lSo2 = len(stato.so2F)//2
    lCo = len(stato.coF)//2
    
    plt.figure(figsize = (12,12))
    plt.title(title)
    plt.plot(stato.no2F[lNo2+1:], stato.no2P[lNo2+1:],'o', label = 'NO2')
    plt.plot(stato.o3F[lO3+1:], stato.o3P[lO3+1:],'o', label = 'O3')
    plt.plot(stato.so2F[lSo2+1:], stato.so2P[lSo2+1:],'o', label = 'SO2')
    plt.plot(stato.coF[lCo+1:], stato.coP[lCo+1:], 'o',label = 'CO')
    plt.grid()
    plt.xlabel('frequenza')
    plt.ylabel('Spettro di potenza')
    plt.legend()
    plt.show()

def plotFftPeriodo2(stato, title):
    lNo2 = len(stato.no2F)//2
    lO3 = len(stato.o3F)//2
    lSo2 = len(stato.so2F)//2
    lCo = len(stato.coF)//2
    
    plt.figure(figsize = (12,12))
    plt.title(title)
    plt.plot(1/(stato.no2F[lNo2+1:]), stato.no2P[lNo2+1:],'o', label = 'NO2')
    plt.plot(1/(stato.o3F[lO3+1:]), stato.o3P[lO3+1:],'o', label = 'O3')
    plt.plot(1/(stato.so2F[lSo2+1:]), stato.so2P[lSo2+1:],'o', label = 'SO2')
    plt.plot(1/(stato.coF[lCo+1:]), stato.coP[lCo+1:], 'o',label = 'CO')
    plt.grid()
    plt.xlabel('periodo')
    plt.ylabel('Spettro di potenza')
    plt.legend()
    plt.show()
            
def originaleVsFiltrato(stato, statoFiltrato, title):
    '''subplot di quattro grafici della concentrazione in funzione del tempo, in ogni grafico è riportato il dato originale e quello filtrato, i quattro grafici corrispondono a un tipo di inquinante diverso'''
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    ax[0][0].plot(stato.date, stato.no2, label= 'originale')
    ax[0][0].plot(statoFiltrato.date, statoFiltrato.no2, label= 'filtrato')
    ax[0][1].plot(stato.date, stato.o3, label= 'originale')
    ax[0][1].plot(statoFiltrato.date, statoFiltrato.o3, label= 'filtrato')
    ax[1][0].plot(stato.date, stato.so2, label= 'originale')
    ax[1][0].plot(statoFiltrato.date, statoFiltrato.so2, label= 'filtrato')
    ax[1][1].plot(stato.date, stato.co, label= 'originale')
    ax[1][1].plot(statoFiltrato.date, statoFiltrato.co, label= 'filtrato')

    ax[0][0].set_xlabel('Time')
    ax[0][0].set_ylabel('NO2 (parts per billion)?')
    ax[0][1].set_xlabel('Time')
    ax[0][1].set_ylabel('O3')
    ax[1][0].set_xlabel('Time')
    ax[1][0].set_ylabel('SO2')
    ax[1][1].set_xlabel('Time')
    ax[1][1].set_ylabel('CO')

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)
    
    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()


    ax[0][0].legend()
    ax[0][1].legend()
    ax[1][0].legend()
    ax[1][1].legend()

    plt.show()



            
def subplotfiltri(stato, statoFiltrato1, statoFiltrato2, statoFiltrato3, statoFiltrato4, filtri):
    '''subplots che mostra per ognuno dei quattro inquinanti di seguito 4 grafici: in ognuno è riportato il dato originale e quello filtrato con un filtro diverso (frequenza che diminuisce di mano a mano)'''

    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle('no2')

    ax[0][0].plot(stato.date, stato.no2, label= 'originale')
    ax[0][0].plot(statoFiltrato1.date, statoFiltrato1.no2, label= 'filtrato f < '+ str(filtri[0]))
    ax[0][1].plot(stato.date, stato.no2, label= 'originale')
    ax[0][1].plot(statoFiltrato1.date, statoFiltrato2.no2, label= 'filtrato f < '+ str(filtri[1]))
    ax[1][0].plot(stato.date, stato.no2, label= 'originale')
    ax[1][0].plot(statoFiltrato1.date, statoFiltrato3.no2, label= 'filtrato f < '+ str(filtri[2]))
    ax[1][1].plot(stato.date, stato.no2, label= 'originale')
    ax[1][1].plot(statoFiltrato1.date, statoFiltrato4.no2, label= 'filtrato f < '+ str(filtri[3]))
    
    ax[0][0].set_xlabel('Time')
    ax[0][0].set_ylabel('NO2')
    ax[0][1].set_xlabel('Time')
    ax[0][1].set_ylabel('NO2')
    ax[1][0].set_xlabel('Time')
    ax[1][0].set_ylabel('NO2')
    ax[1][1].set_xlabel('Time')
    ax[1][1].set_ylabel('NO2')

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)
    
    ax[0][0].legend()
    ax[0][1].legend()
    ax[1][0].legend()
    ax[1][1].legend()

    plt.show()
    
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle('o3')
    ax[0][0].plot(stato.date, stato.o3, label= 'originale')
    ax[0][0].plot(statoFiltrato1.date, statoFiltrato1.o3, label= 'filtrato f < '+str(filtri[0]))
    ax[0][1].plot(stato.date, stato.o3, label= 'originale')
    ax[0][1].plot(statoFiltrato2.date, statoFiltrato2.o3, label= 'filtrato f < '+str(filtri[1]))
    ax[1][0].plot(stato.date, stato.o3, label= 'originale')
    ax[1][0].plot(statoFiltrato3.date, statoFiltrato3.o3, label= 'filtrato f < '+str(filtri[2]))
    ax[1][1].plot(stato.date, stato.o3, label= 'originale')
    ax[1][1].plot(statoFiltrato4.date, statoFiltrato4.o3, label= 'filtrato f < '+str(filtri[3]))

    ax[0][0].set_xlabel('Time')
    ax[0][0].set_ylabel('O3')
    ax[0][1].set_xlabel('Time')
    ax[0][1].set_ylabel('O3')
    ax[1][0].set_xlabel('Time')
    ax[1][0].set_ylabel('O3')
    ax[1][1].set_xlabel('Time')
    ax[1][1].set_ylabel('O3')

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)
    
    ax[0][0].legend()
    ax[0][1].legend()
    ax[1][0].legend()
    ax[1][1].legend()

    plt.show()

    fig,ax = plt.subplots(2,2, figsize = (36,12))
    fig.suptitle('so2')
    ax[0][0].plot(stato.date, stato.so2, label= 'originale')
    ax[0][0].plot(statoFiltrato1.date, statoFiltrato1.so2, label= 'filtrato f < '+str(filtri[0]))
    ax[0][1].plot(stato.date, stato.so2, label= 'originale')
    ax[0][1].plot(statoFiltrato2.date, statoFiltrato2.so2, label= 'filtrato f < '+str(filtri[1]))
    ax[1][0].plot(stato.date, stato.so2, label= 'originale')
    ax[1][0].plot(statoFiltrato3.date, statoFiltrato3.so2, label= 'filtrato f < '+str(filtri[2]))
    ax[1][1].plot(stato.date, stato.so2, label= 'originale')
    ax[1][1].plot(statoFiltrato4.date, statoFiltrato4.so2, label= 'filtrato f < '+str(filtri[3]))

    ax[0][0].set_xlabel('Time')
    ax[0][0].set_ylabel('SO2')
    ax[0][1].set_xlabel('Time')
    ax[0][1].set_ylabel('SO2')
    ax[1][0].set_xlabel('Time')
    ax[1][0].set_ylabel('SO2')
    ax[1][1].set_xlabel('Time')
    ax[1][1].set_ylabel('SO2')
    
    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)

    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()

    ax[0][0].legend()
    ax[0][1].legend()
    ax[1][0].legend()
    ax[1][1].legend()

    plt.show()

    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle('co')
    ax[0][0].plot(stato.date, stato.co, label= 'originale')
    ax[0][0].plot(statoFiltrato1.date, statoFiltrato1.co, label= 'filtrato f < '+str(filtri[0]))
    ax[0][1].plot(stato.date, stato.co, label= 'originale')
    ax[0][1].plot(statoFiltrato2.date, statoFiltrato2.co, label= 'filtrato f < '+str(filtri[1]))
    ax[1][0].plot(stato.date, stato.co, label= 'originale')
    ax[1][0].plot(statoFiltrato3.date, statoFiltrato3.co, label= 'filtrato f < '+str(filtri[2]))
    ax[1][1].plot(stato.date, stato.co, label= 'originale')
    ax[1][1].plot(statoFiltrato4.date, statoFiltrato4.co, label= 'filtrato f < '+str(filtri[3]))

    ax[0][0].set_xlabel('Time')
    ax[0][0].set_ylabel('CO')
    ax[0][1].set_xlabel('Time')
    ax[0][1].set_ylabel('CO')
    ax[1][0].set_xlabel('Time')
    ax[1][0].set_ylabel('CO')
    ax[1][1].set_xlabel('Time')
    ax[1][1].set_ylabel('CO')

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)

    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()

    ax[0][0].legend()
    ax[0][1].legend()
    ax[1][0].legend()
    ax[1][1].legend()

    plt.show()
    
    
#---------------------------------------------------------------#
#       Definizione moduli grafici per analisi Stazioni         #
#---------------------------------------------------------------#

def subplotInquinanti(stato, title):
    
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    for i in range(len(stato.siteNum)):
        ax[0][0].plot(stato.sites[i].date, stato.sites[i].no2, label = 'site num ' + str(stato.siteNum[i]), alpha = 0.6)
        ax[0][1].plot(stato.sites[i].date, stato.sites[i].o3, alpha = 0.6)
        ax[1][0].plot(stato.sites[i].date, stato.sites[i].so2, alpha = 0.6)
        ax[1][1].plot(stato.sites[i].date, stato.sites[i].co, alpha = 0.6)

    ax[0][0].set_xlabel('Time')
    ax[0][0].set_ylabel('NO2')
    ax[0][1].set_xlabel('Time')
    ax[0][1].set_ylabel('O3')
    ax[1][0].set_xlabel('Time')
    ax[1][0].set_ylabel('SO2')
    ax[1][1].set_xlabel('Time')
    ax[1][1].set_ylabel('CO')

    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)

    fig.legend()
    
    plt.show()


def subplotInquinantiFft(stato, title):
    
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    for i in range(len(stato.siteNumFft)):
        ax[0][0].plot(stato.sitesFft[i].no2F[1:], stato.sitesFft[i].no2P[1:], label = 'site num ' + str(stato.siteNumFft[i]), alpha = 0.6)
        ax[0][1].plot(stato.sitesFft[i].o3F[1:], stato.sitesFft[i].o3P[1:], alpha = 0.6)
        ax[1][0].plot(stato.sitesFft[i].so2F[1:], stato.sitesFft[i].so2P[1:], alpha = 0.6)
        ax[1][1].plot(stato.sitesFft[i].coF[1:], stato.sitesFft[i].coP[1:], alpha = 0.6)

    ax[0][0].set_xlabel('Frequenza')
    ax[0][0].set_ylabel('Spettro di potenza NO2')
    ax[0][1].set_xlabel('Frequenza')
    ax[0][1].set_ylabel('Spettro di potenza O3')
    ax[1][0].set_xlabel('Frequenza')
    ax[1][0].set_ylabel('Spettro di potenza SO2')
    ax[1][1].set_xlabel('Frequenza')
    ax[1][1].set_ylabel('Spettro di potenza CO')

    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)

    fig.legend()
    
    plt.show()

