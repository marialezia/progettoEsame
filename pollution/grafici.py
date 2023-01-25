import pandas as pd
import numpy as np
import classi as cl
import sys, os
from tqdm import tqdm
import matplotlib.pyplot as plt

#---------------------------------------------------------------#
#               Descrizione contenuto codice                    #
#---------------------------------------------------------------#
'''
Nel seguente file sono contenute le definizioni di funzioni per la produzione di diversi grafici, si distinguno a seconda dell'uso per l'analisi Stati, l'analisi Stazioni o l'analisi Inquinanti. 
'''
#---------------------------------------------------------------#
#       Definizione moduli grafici per analisi Stati            #
#---------------------------------------------------------------#

def subplotInquinantiScale(stato, title):
    #produce il grafico della concentrazione degli inquinanti in funzione del tempo, sia in scala normale che in scala logaritmica
    fig,ax = plt.subplots(2,1, figsize = (24,6))
    fig.suptitle(title)

    ax[0].plot(stato.days, stato.no2,label= 'NO2')
    ax[0].plot(stato.days, stato.o3, label = 'O3')
    ax[0].plot(stato.days, stato.so2, label = 'SO2')
    ax[0].plot(stato.days, stato.co,  label = 'CO')
    ax[0].set_xlabel('Time [d]', size = 10)
    ax[0].set_ylabel('Concentrazione media [ppm]')
    ax[0].legend()

    ax[1].plot(stato.days, stato.no2,label= 'NO2')
    ax[1].plot(stato.days, stato.o3, label = 'O3')
    ax[1].plot(stato.days, stato.so2, label = 'SO2')
    ax[1].plot(stato.days, stato.co,  label = 'CO')
    ax[1].set_xlabel('Time [D]', size = 10)
    ax[1].set_ylabel('Concentrazione media [ppm]')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    ax[1].legend()
    plt.show()

def subplotFftScale(stato, title, zero):
    #produce il grafico dello spettro di potenza degli inquinanti in funzione delle frequenze, sia in scala normale che in scala logaritmiza, si può scegliere se includere o no il termine corrispondente alla Frequenza [1/d] zero. Per includerlo devo mettere zero == True
    fig,ax = plt.subplots(2,1, figsize = (12,12))
    fig.suptitle(title)
    if zero == True: 
        ax[0].plot(stato.no2F, stato.no2P,label= 'NO2')
        ax[0].plot(stato.o3F, stato.o3P, label = 'O3')
        ax[0].plot(stato.so2F, stato.so2P, label = 'SO2')
        ax[0].plot(stato.coF, stato.coP,  label = 'CO')
        ax[1].plot(stato.no2F, stato.no2P,label= 'NO2')
        ax[1].plot(stato.o3F, stato.o3P, label = 'O3')
        ax[1].plot(stato.so2F, stato.so2P, label = 'SO2')
        ax[1].plot(stato.coF, stato.coP,  label = 'CO')
    else:
        ax[0].plot(stato.no2F[1:], stato.no2P[1:],label= 'NO2')
        ax[0].plot(stato.o3F[1:], stato.o3P[1:], label = 'O3')
        ax[0].plot(stato.so2F[1:], stato.so2P[1:], label = 'SO2')
        ax[0].plot(stato.coF[1:], stato.coP[1:],  label = 'CO')
        ax[1].plot(stato.no2F[1:], stato.no2P[1:],label= 'NO2')
        ax[1].plot(stato.o3F[1:], stato.o3P[1:], label = 'O3')
        ax[1].plot(stato.so2F[1:], stato.so2P[1:], label = 'SO2')
        ax[1].plot(stato.coF[1:], stato.coP[1:],  label = 'CO')
        
    ax[0].set_xlabel('Frequenza [1/D]', size = 10)
    ax[0].set_ylabel('Spettro di potenza')
    ax[0].legend()
    ax[1].set_xlabel('Frequenza [1/D]', size = 10)
    ax[1].set_ylabel('Spettro di Potenza')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    ax[1].legend()
    plt.show()

def subplotFftScalePeriodo(stato, title, massimo, maxValues):
     #produce il grafico dello spettro di potenza degli inquinanti in funzione del periodo, sia in scala normale che in scala logaritmiza, se massimo = True viene visualizzato anche il massimo
    
    fig,ax = plt.subplots(2,1, figsize = (12,12))
    fig.suptitle(title)

    ax[0].plot(1/stato.no2F[1:], stato.no2P[1:], color = 'blue', label= 'NO2')
    ax[0].plot(1/stato.o3F[1:], stato.o3P[1:], color = 'springgreen',  label = 'O3')
    ax[0].plot(1/stato.so2F[1:], stato.so2P[1:], color = 'rebeccapurple', label = 'SO2')
    ax[0].plot(1/stato.coF[1:], stato.coP[1:], color = 'salmon', label = 'CO')
    ax[0].set_xlabel('Periodo [D]', size = 10)
    ax[0].set_ylabel('Spettro di potenza')
    ax[0].legend()

    ax[1].plot(1/stato.no2F[1:], stato.no2P[1:], color = 'blue',label= 'NO2')
    ax[1].plot(1/stato.o3F[1:], stato.o3P[1:], color = 'springgreen', label = 'O3')
    ax[1].plot(1/stato.so2F[1:], stato.so2P[1:], color = 'rebeccapurple', label = 'SO2')
    ax[1].plot(1/stato.coF[1:], stato.coP[1:], color = 'salmon',  label = 'CO')
    
    ax[1].set_xlabel('Periodo [d]', size = 10)
    ax[1].set_ylabel('Spettro di Potenza')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    ax[1].legend()

    if massimo == True:
            ax[0].plot(1/stato.no2F[1:][maxValues[0]], stato.no2P[1:][maxValues[0]], 'o', color = 'blue', label= 'NO2')
            ax[0].plot(1/stato.o3F[1:][maxValues[1]], stato.o3P[1:][maxValues[1]],'o', color = 'springgreen',label = 'O3')
            ax[0].plot(1/stato.so2F[1:][maxValues[2]], stato.so2P[1:][maxValues[2]],'o', color = 'rebeccapurple',label = 'SO2')
            ax[0].plot(1/stato.coF[1:][maxValues[3]], stato.coP[1:][maxValues[3]], 'o', color = 'salmon',label = 'CO')
            ax[1].plot(1/stato.no2F[1:][maxValues[0]], stato.no2P[1:][maxValues[0]], 'o', color = 'blue',label= 'NO2')
            ax[1].plot(1/stato.o3F[1:][maxValues[1]], stato.o3P[1:][maxValues[1]],  'o', color = 'springgreen',label = 'O3')
            ax[1].plot(1/stato.so2F[1:][maxValues[2]], stato.so2P[1:][maxValues[2]],  'o', color = 'rebeccapurple',label = 'SO2')
            ax[1].plot(1/stato.coF[1:][maxValues[3]], stato.coP[1:][maxValues[3]],   'o', color = 'salmon',label = 'CO')
    plt.show()

            
def originaleVsFiltrato(stato, statoFiltrato, title, scale):
    '''subplot di quattro grafici della Concentrazione media [ppm] in funzione del tempo, in ogni grafico è riportato il dato originale e quello filtrato, i quattro grafici corrispondono a un tipo di inquinante diverso'''
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    ax[0][0].plot(stato.days, stato.no2, label= 'originale')
    ax[0][0].plot(statoFiltrato.days, statoFiltrato.no2, label= 'filtrato')
    ax[0][1].plot(stato.days, stato.o3, label= 'originale')
    ax[0][1].plot(statoFiltrato.days, statoFiltrato.o3, label= 'filtrato')
    ax[1][0].plot(stato.days, stato.so2, label= 'originale')
    ax[1][0].plot(statoFiltrato.days, statoFiltrato.so2, label= 'filtrato')
    ax[1][1].plot(stato.days, stato.co, label= 'originale')
    ax[1][1].plot(statoFiltrato.days, statoFiltrato.co, label= 'filtrato')

    ax[0][0].set_xlabel('Time [D]')
    ax[0][0].set_ylabel('NO2 (parts per billion)?')
    ax[0][1].set_xlabel('Time [D]')
    ax[0][1].set_ylabel('O3')
    ax[1][0].set_xlabel('Time [D]')
    ax[1][0].set_ylabel('SO2')
    ax[1][1].set_xlabel('Time [D]')
    ax[1][1].set_ylabel('CO')

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)
    
    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()

    if scale == 'log':
        ax[0][0].set_xscale('log')
        ax[0][0].set_yscale('log')
        ax[0][1].set_xscale('log')
        ax[0][1].set_yscale('log')
        ax[1][0].set_xscale('log')
        ax[1][0].set_yscale('log')
        ax[1][1].set_xscale('log')
        ax[1][1].set_yscale('log')

    ax[0][0].legend()
    ax[0][1].legend()
    ax[1][0].legend()
    ax[1][1].legend()

    plt.show()



            
def subplotfiltri(stato, statoFiltrato1, statoFiltrato2, statoFiltrato3, statoFiltrato4, filtri):
    '''subplots che mostra per ognuno dei quattro inquinanti di seguito 4 grafici: in ognuno è riportato il dato originale e quello filtrato con un filtro diverso (Frequenza [1/d] che diminuisce di mano a mano)'''

    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle('no2')

    ax[0][0].plot(stato.days, stato.no2, label= 'originale')
    ax[0][0].plot(statoFiltrato1.days, statoFiltrato1.no2, label= 'filtrato f < '+ str(filtri[0]))
    ax[0][1].plot(stato.days, stato.no2, label= 'originale')
    ax[0][1].plot(statoFiltrato1.days, statoFiltrato2.no2, label= 'filtrato f < '+ str(filtri[1]))
    ax[1][0].plot(stato.days, stato.no2, label= 'originale')
    ax[1][0].plot(statoFiltrato1.days, statoFiltrato3.no2, label= 'filtrato f < '+ str(filtri[2]))
    ax[1][1].plot(stato.days, stato.no2, label= 'originale')
    ax[1][1].plot(statoFiltrato1.days, statoFiltrato4.no2, label= 'filtrato f < '+ str(filtri[3]))
    
    ax[0][0].set_xlabel('Time [D]')
    ax[0][0].set_ylabel('NO2')
    ax[0][1].set_xlabel('Time [D]')
    ax[0][1].set_ylabel('NO2')
    ax[1][0].set_xlabel('Time [D]')
    ax[1][0].set_ylabel('NO2')
    ax[1][1].set_xlabel('Time [D]')
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
    ax[0][0].plot(stato.days, stato.o3, label= 'originale')
    ax[0][0].plot(statoFiltrato1.days, statoFiltrato1.o3, label= 'filtrato f < '+str(filtri[0]))
    ax[0][1].plot(stato.days, stato.o3, label= 'originale')
    ax[0][1].plot(statoFiltrato2.days, statoFiltrato2.o3, label= 'filtrato f < '+str(filtri[1]))
    ax[1][0].plot(stato.days, stato.o3, label= 'originale')
    ax[1][0].plot(statoFiltrato3.days, statoFiltrato3.o3, label= 'filtrato f < '+str(filtri[2]))
    ax[1][1].plot(stato.days, stato.o3, label= 'originale')
    ax[1][1].plot(statoFiltrato4.days, statoFiltrato4.o3, label= 'filtrato f < '+str(filtri[3]))

    ax[0][0].set_xlabel('Time [D]')
    ax[0][0].set_ylabel('O3')
    ax[0][1].set_xlabel('Time [D]')
    ax[0][1].set_ylabel('O3')
    ax[1][0].set_xlabel('Time [D]')
    ax[1][0].set_ylabel('O3')
    ax[1][1].set_xlabel('Time [D]')
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
    ax[0][0].plot(stato.days, stato.so2, label= 'originale')
    ax[0][0].plot(statoFiltrato1.days, statoFiltrato1.so2, label= 'filtrato f < '+str(filtri[0]))
    ax[0][1].plot(stato.days, stato.so2, label= 'originale')
    ax[0][1].plot(statoFiltrato2.days, statoFiltrato2.so2, label= 'filtrato f < '+str(filtri[1]))
    ax[1][0].plot(stato.days, stato.so2, label= 'originale')
    ax[1][0].plot(statoFiltrato3.days, statoFiltrato3.so2, label= 'filtrato f < '+str(filtri[2]))
    ax[1][1].plot(stato.days, stato.so2, label= 'originale')
    ax[1][1].plot(statoFiltrato4.days, statoFiltrato4.so2, label= 'filtrato f < '+str(filtri[3]))

    ax[0][0].set_xlabel('Time [D]')
    ax[0][0].set_ylabel('SO2')
    ax[0][1].set_xlabel('Time [D]')
    ax[0][1].set_ylabel('SO2')
    ax[1][0].set_xlabel('Time [D]')
    ax[1][0].set_ylabel('SO2')
    ax[1][1].set_xlabel('Time [D]')
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
    ax[0][0].plot(stato.days, stato.co, label= 'originale')
    ax[0][0].plot(statoFiltrato1.days, statoFiltrato1.co, label= 'filtrato f < '+str(filtri[0]))
    ax[0][1].plot(stato.days, stato.co, label= 'originale')
    ax[0][1].plot(statoFiltrato2.days, statoFiltrato2.co, label= 'filtrato f < '+str(filtri[1]))
    ax[1][0].plot(stato.days, stato.co, label= 'originale')
    ax[1][0].plot(statoFiltrato3.days, statoFiltrato3.co, label= 'filtrato f < '+str(filtri[2]))
    ax[1][1].plot(stato.days, stato.co, label= 'originale')
    ax[1][1].plot(statoFiltrato4.days, statoFiltrato4.co, label= 'filtrato f < '+str(filtri[3]))

    ax[0][0].set_xlabel('Time [D]')
    ax[0][0].set_ylabel('CO')
    ax[0][1].set_xlabel('Time [D]')
    ax[0][1].set_ylabel('CO')
    ax[1][0].set_xlabel('Time [D]')
    ax[1][0].set_ylabel('CO')
    ax[1][1].set_xlabel('Time [D]')
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
    
def graficoTuttiStati(s1,s1Name, s2, s2Name, s3,s3Name, s4, s4Name, s5, s5Name, title):
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    ax[0][0].plot(s1.date, s1.no2, label= s1Name)
    ax[0][0].plot(s2.date, s2.no2, label= s2Name)
    ax[0][0].plot(s3.date, s3.no2, label= s3Name)
    ax[0][0].plot(s4.date, s4.no2, label= s4Name)
    ax[0][0].plot(s5.date, s5.no2, label= s5Name)
    
    ax[0][1].plot(s1.date, s1.o3, label= s1Name)
    ax[0][1].plot(s2.date, s2.o3, label= s2Name)
    ax[0][1].plot(s3.date, s3.o3, label= s3Name)
    ax[0][1].plot(s4.date, s4.o3, label= s4Name)
    ax[0][1].plot(s5.date, s5.o3, label= s5Name)

    ax[1][0].plot(s1.date, s1.so2, label= s1Name)
    ax[1][0].plot(s2.date, s2.so2, label= s2Name)
    ax[1][0].plot(s3.date, s3.so2, label= s3Name)
    ax[1][0].plot(s4.date, s4.so2, label= s4Name)
    ax[1][0].plot(s5.date, s5.so2, label= s5Name)

    ax[1][1].plot(s1.date, s1.co, label= s1Name)
    ax[1][1].plot(s2.date, s2.co, label= s2Name)
    ax[1][1].plot(s3.date, s3.co, label= s3Name)
    ax[1][1].plot(s4.date, s4.co, label= s4Name)
    ax[1][1].plot(s5.date, s5.co, label= s5Name)

    ax[0][0].set_xlabel('Time [D]')
    ax[0][0].set_ylabel('NO2 (parts per billion)?')
    ax[0][1].set_xlabel('Time [D]')
    ax[0][1].set_ylabel('O3')
    ax[1][0].set_xlabel('Time [D]')
    ax[1][0].set_ylabel('SO2')
    ax[1][1].set_xlabel('Time [D]')
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

    ax[0][0].set_xlabel('Time [D]')
    ax[0][0].set_ylabel('NO2')
    ax[0][1].set_xlabel('Time [D]')
    ax[0][1].set_ylabel('O3')
    ax[1][0].set_xlabel('Time [D]')
    ax[1][0].set_ylabel('SO2')
    ax[1][1].set_xlabel('Time [D]')
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

    ax[0][0].set_xlabel('Frequenza [1/D]')
    ax[0][0].set_ylabel('Spettro di potenza NO2')
    ax[0][1].set_xlabel('Frequenza [1/D]')
    ax[0][1].set_ylabel('Spettro di potenza O3')
    ax[1][0].set_xlabel('Frequenza [1/D]')
    ax[1][0].set_ylabel('Spettro di potenza SO2')
    ax[1][1].set_xlabel('Frequenza [1/D]')
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




#---------------------------------------------------------------#
#       Definizione moduli grafici VECCHI                       #
#---------------------------------------------------------------#

    
def plotFft2(stato, title, scale):
    lNo2 = len(stato.no2F)//2
    lO3 = len(stato.o3F)//2
    lSo2 = len(stato.so2F)//2
    lCo = len(stato.coF)//2
    
    plt.figure(figsize = (12,12))
    plt.title(title)
    plt.plot(stato.no2F[lNo2+1:], stato.no2P[lNo2+1:],label = 'NO2')
    plt.plot(stato.o3F[lO3+1:], stato.o3P[lO3+1:], label = 'O3')
    plt.plot(stato.so2F[lSo2+1:], stato.so2P[lSo2+1:],label = 'SO2')
    plt.plot(stato.coF[lCo+1:], stato.coP[lCo+1:],label = 'CO')
    plt.grid()
    plt.xlabel('Frequenza [1/d]')
    plt.ylabel('Spettro di potenza')
    if scale == 'log':
        plt.xscale('log')
        plt.yscale('log')
    plt.legend()
    plt.show()

def plotFftPeriodo2(stato, title, scale):
    lNo2 = len(stato.no2F)//2
    lO3 = len(stato.o3F)//2
    lSo2 = len(stato.so2F)//2
    lCo = len(stato.coF)//2
    
    plt.figure(figsize = (12,12))
    plt.title(title)
    plt.plot(1/(stato.no2F[lNo2+1:]), stato.no2P[lNo2+1:], label = 'NO2')
    plt.plot(1/(stato.o3F[lO3+1:]), stato.o3P[lO3+1:], label = 'O3')
    plt.plot(1/(stato.so2F[lSo2+1:]), stato.so2P[lSo2+1:], label = 'SO2')
    plt.plot(1/(stato.coF[lCo+1:]), stato.coP[lCo+1:],label = 'CO')
    plt.grid()
    plt.xlabel('periodo')
    plt.ylabel('Spettro di potenza')
    if scale == 'log':
        plt.xscale('log')
        plt.yscale('log')
    plt.legend()
    plt.show()


def plotInquinanti2(stato, title, scale):
    plt.figure(figsize = (12,12))
    plt.title(title)
    plt.plot(stato.days, stato.no2,label= 'NO2')
    plt.plot(stato.days, stato.o3, label = 'O3')
    plt.plot(stato.days, stato.so2, label = 'SO2')
    plt.plot(stato.days, stato.co,  label = 'CO')
    plt.grid()
    plt.xlabel('Time [D]', size = 10)
    plt.ylabel('Concentrazione media [ppm]')
    if scale == 'log':
        plt.xscale('log')
        plt.yscale('log')
    plt.legend()
    plt.show()
