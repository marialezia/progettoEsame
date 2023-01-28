import pandas as pd
import funzioni as fz
import numpy as np
import classi as cl
import sys, os
from tqdm import tqdm
import matplotlib.pyplot as plt

'''
Nel seguente file sono contenute le definizioni di funzioni per la produzione di diversi grafici, si distinguno a seconda dell'uso per l'analisi Stati, l'analisi Stazioni o l'analisi Inquinanti. 
'''
#---------------------------------------------------------------#
#       Definizione moduli grafici per analisi Stati            #
#---------------------------------------------------------------#

def plotInquinanti2(stato, title, name):
    '''
    Produce il grafico della concentrazione degli inquinanti in funzione del tempo.
    Salva la figura all'interno della cartella corrispondente allo stato all'interno di datiSalvati/analisiStati.
    Parametri:
    stato: di tipo classe Stato, stato di cui fare il grafico
    title: stringa, titolo del grafico
    name: stringa, nome dello stato
    '''
    plt.figure(figsize = (12,12))
    plt.title(title)
    plt.plot(stato.date, stato.no2, label= 'NO2')
    plt.plot(stato.date, stato.so2, label = 'SO2')
    plt.plot(stato.date, stato.co,  label = 'CO')
    plt.plot(stato.date, stato.o3, label = 'O3')
    plt.grid()
    plt.xlabel('Tempo [d]', size = 10)
    plt.ylabel('Concentrazione media [ppm]')
    plt.legend()
    plt.show()
    
def subplotInquinantiScale(stato, title, name, nFile):
    '''
    Produce il grafico della concentrazione degli inquinanti in funzione del tempo, sia in scala normale che in scala logaritmica.
    Salva la figura all'interno della cartella corrispondente allo stato all'interno di datiSalvati/analisiStati.
    Parametri:
    stato: di tipo classe Stato, stato di cui fare il grafico
    title: stringa, titolo del grafico
    name: stringa, nome dello stato
    nFile: stringa, nome con cui viene salvato il file
    '''
    fig,ax = plt.subplots(2,1, figsize = (18,12))
    fig.suptitle(title)

    ax[0].plot(stato.days, stato.no2,label= 'NO2')
    ax[0].plot(stato.days, stato.o3, label = 'O3')
    ax[0].plot(stato.days, stato.so2, label = 'SO2')
    ax[0].plot(stato.days, stato.co,  label = 'CO')
    ax[0].set_xlabel('Tempo [d]', size = 10)
    ax[0].set_ylabel('Concentration media [ppm]')
    ax[0].legend()

    ax[1].plot(stato.days, stato.no2,label= 'NO2')
    ax[1].plot(stato.days, stato.o3, label = 'O3')
    ax[1].plot(stato.days, stato.so2, label = 'SO2')
    ax[1].plot(stato.days, stato.co,  label = 'CO')
    ax[1].set_xlabel('log(Tempo [d])', size = 10)
    ax[1].set_ylabel('log(Concentrazione media [ppm])')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    ax[1].legend()
    currentDirectory = os.getcwd()
    plt.savefig(currentDirectory +'/datiSalvati/analisiStati/' + name + nFile)
    plt.show()

def subplotFftScale(stato, title, name, zero):
    '''
    Produce il grafico dello spettro di potenza degli inquinanti in funzione delle frequenze, sia in scala normale che in scala logaritmiza, si può scegliere se includere o no il termine corrispondente alla Frequenza zero. 
    Salva la figura all'interno della cartella corrispondente allo stato all'interno di datiSalvati/analisiStati.
    Parametri:
    stato: di tipo classe Stato, stato di cui fare il grafico
    title: stringa, titolo del grafico
    name: stringa, nome dello stato
    zero: booleana, se è True viene incluso il termine corrispondete alla frequenza zero 
    '''
    
    fig,ax = plt.subplots(2,1, figsize = (18,12))
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
        
    ax[0].set_xlabel('Frequenza [1/d]', size = 10)
    ax[0].set_ylabel('Spettro di potenza')
    ax[0].legend()
    ax[1].set_xlabel('log(Frequenza [1/d])', size = 10)
    ax[1].set_ylabel('log(Spettro di Potenza)')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    ax[1].legend()
    
    currentDirectory = os.getcwd()
    if zero == True:
        plt.savefig(currentDirectory +'/datiSalvati/analisiStati/' + name + '/spetPotFreq' + name + 'F0.png')
    else:        
        plt.savefig(currentDirectory +'/datiSalvati/analisiStati/' + name + '/spetPotFreq' + name + '.png')
    plt.show()

def subplotFftNorm(stato, title, name, norm):
    '''
    Produce il grafico dello spettro di potenza degli inquinanti in funzione delle frequenze, sia in scala normale che in scala logaritmiza, si può scegliere se includere o no il termine corrispondente alla Frequenza zero. 
    Salva la figura all'interno della cartella corrispondente allo stato all'interno di datiSalvati/analisiStati.
    Parametri:
    stato: di tipo classe Stato, stato di cui fare il grafico
    title: stringa, titolo del grafico
    name: stringa, nome dello stato
    zero: booleana, se è True viene incluso il termine corrispondete alla frequenza zero 
    '''
    
    fig,ax = plt.subplots(2,1, figsize = (18,12))
    fig.suptitle(title)
   
    ax[0].plot(stato.no2F[1:], stato.no2P[1:]/norm[0],label= 'NO2')
    ax[0].plot(stato.o3F[1:], stato.o3P[1:]/norm[1], label = 'O3')
    ax[0].plot(stato.so2F[1:], stato.so2P[1:]/norm[2], label = 'SO2')
    ax[0].plot(stato.coF[1:], stato.coP[1:]/norm[3],  label = 'CO')
    ax[1].plot(stato.no2F[1:], stato.no2P[1:]/norm[0],label= 'NO2')
    ax[1].plot(stato.o3F[1:], stato.o3P[1:]/norm[1], label = 'O3')
    ax[1].plot(stato.so2F[1:], stato.so2P[1:]/norm[2], label = 'SO2')
    ax[1].plot(stato.coF[1:], stato.coP[1:]/norm[3],  label = 'CO')
        
    ax[0].set_xlabel('Frequenza [1/d]', size = 10)
    ax[0].set_ylabel('Spettro di potenza')
    ax[0].legend()
    ax[1].set_xlabel('log(Frequenza [1/d])', size = 10)
    ax[1].set_ylabel('log(Spettro di Potenza)')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    ax[1].legend()
    
    currentDirectory = os.getcwd()        
    plt.savefig(currentDirectory +'/datiSalvati/analisiStati/' + name + '/spetPotNorm' + name + '.png')
    plt.show()

def subplotFftScalePeriodo(stato, title, name, massimo, maxValues):
    '''
    Produce il grafico dello spettro di potenza degli inquinanti in funzione dei periodi, sia in scala normale che in scala logaritmiza, si può scegliere se mostrare o no il punto in cui lo spettro di potenza è massimo. 
    Salva la figura all'interno della cartella corrispondente allo stato all'interno di datiSalvati/analisiStati.
    Parametri:
    stato: di tipo classe Stato, stato di cui fare il grafico
    title: stringa, titolo del grafico
    name: stringa, nome dello stato
    massimo: booleana, se è True viene mostrato il massimo
    maxValues: array di interi, contiene gli indici delle posizioni dei massimi per ogni inquinante
    '''
    
    fig,ax = plt.subplots(2,1, figsize = (18,12))
    fig.suptitle(title)

    ax[0].plot(1/stato.no2F[1:], stato.no2P[1:], color = 'blue', label= 'NO2')
    ax[0].plot(1/stato.o3F[1:], stato.o3P[1:], color = 'springgreen',  label = 'O3')
    ax[0].plot(1/stato.so2F[1:], stato.so2P[1:], color = 'rebeccapurple', label = 'SO2')
    ax[0].plot(1/stato.coF[1:], stato.coP[1:], color = 'salmon', label = 'CO')
    ax[0].set_xlabel('Periodo [d]', size = 10)
    ax[0].set_ylabel('Spettro di potenza')
    ax[0].legend()

    ax[1].plot(1/stato.no2F[1:], stato.no2P[1:], color = 'blue',label= 'NO2')
    ax[1].plot(1/stato.o3F[1:], stato.o3P[1:], color = 'springgreen', label = 'O3')
    ax[1].plot(1/stato.so2F[1:], stato.so2P[1:], color = 'rebeccapurple', label = 'SO2')
    ax[1].plot(1/stato.coF[1:], stato.coP[1:], color = 'salmon',  label = 'CO')
    
    ax[1].set_xlabel('log(Periodo [d])', size = 10)
    ax[1].set_ylabel('log(Spettro di Potenza)')
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

    currentDirectory = os.getcwd()
    if massimo == True:
        plt.savefig(currentDirectory +'/datiSalvati/analisiStati/' + name + '/spetPotPer' + name + 'M.png')
    else:        
        plt.savefig(currentDirectory +'/datiSalvati/analisiStati/' + name + '/spetPotPer' + name + '.png')
    plt.show()

            
def originaleVsFiltrato(stato, statoFiltrato, title, name, filtro):
    '''
    Produce un subplot di quattro grafici della concentrazione media degli inquinanti in funzione del tempo, in ogni grafico è riportato il dato originale e quello filtrato.  
    Salva la figura all'interno della cartella corrispondente allo stato all'interno di datiSalvati/analisiStati.
    Parametri:
    stato: di tipo classe Stato, contiene dati originali
    statoFiltrato: di tipo classe Stato, contiene i dati filtrati
    title: stringa, titolo del grafico
    name: stringa, nome dello stato
    filtro: reale, frequenza di filtro
    scale: stringa, se scale = 'log' i grafici sono in scala logaritminca
    '''
    fig,ax = plt.subplots(2,2, figsize = (18,12))
    fig.suptitle(title)

    ax[0][0].plot(stato.date, stato.no2, label= 'originale')
    ax[0][0].plot(statoFiltrato.date, statoFiltrato.no2, label= 'filtrato')
    ax[0][1].plot(stato.date, stato.o3, label= 'originale')
    ax[0][1].plot(statoFiltrato.date, statoFiltrato.o3, label= 'filtrato')
    ax[1][0].plot(stato.date, stato.so2, label= 'originale')
    ax[1][0].plot(statoFiltrato.date, statoFiltrato.so2, label= 'filtrato')
    ax[1][1].plot(stato.date, stato.co, label= 'originale')
    ax[1][1].plot(statoFiltrato.date, statoFiltrato.co, label= 'filtrato')

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)
    
    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()

    ax[0][0].set_xlabel('Tempo [d]')
    ax[0][0].set_ylabel('Concentrazione media NO2 [ppm]')
    ax[0][1].set_xlabel('Tempo [d]')
    ax[0][1].set_ylabel('Concentrazione media O3 [ppm]')
    ax[1][0].set_xlabel('Tempo [d]')
    ax[1][0].set_ylabel('Concentrazione media SO2 [ppm]')
    ax[1][1].set_xlabel('Tempo [d]')
    ax[1][1].set_ylabel('Concentrazione media CO [ppm]')

    ax[0][0].legend()
    ax[0][1].legend()
    ax[1][0].legend()
    ax[1][1].legend()

    currentDirectory = os.getcwd()
    plt.savefig(currentDirectory +'/datiSalvati/analisiStati/' +  name + '/orVsFil' + str(filtro) + name + '.png')
    plt.show()

def subplotFiltri(statoFiltrato1, statoFiltrato2, statoFiltrato3, statoFiltrato4, name, filtri):
    fig,ax = plt.subplots(2,2, figsize = (18,12))
    fig.suptitle('Analisi ' + name + ': confronto filtri')

    ax[0][0].plot(statoFiltrato1.date, statoFiltrato1.no2,alpha = 0.8, label= 'no2')
    ax[0][0].plot(statoFiltrato1.date, statoFiltrato1.o3,alpha = 0.8, label= 'o3')
    ax[0][0].plot(statoFiltrato1.date, statoFiltrato1.so2,alpha = 0.8, label= 'so2')
    ax[0][0].plot(statoFiltrato1.date, statoFiltrato1.co,alpha = 0.8, label= 'co')
    ax[0][0].set_title('filtrato f < ' + str(filtri[0])+ ' $d^{-1}$')

    ax[0][1].plot(statoFiltrato2.date, statoFiltrato2.no2,alpha = 0.8, label= 'no2')
    ax[0][1].plot(statoFiltrato2.date, statoFiltrato2.o3,alpha = 0.8, label= 'o3')
    ax[0][1].plot(statoFiltrato2.date, statoFiltrato2.so2,alpha = 0.8, label= 'so2')
    ax[0][1].plot(statoFiltrato2.date, statoFiltrato2.co,alpha = 0.8, label= 'co')
    ax[0][1].set_title('filtrato f < ' + str(filtri[1])+ ' $d^{-1}$')

    ax[1][0].plot(statoFiltrato3.date, statoFiltrato3.no2,alpha = 0.8, label= 'no2')
    ax[1][0].plot(statoFiltrato3.date, statoFiltrato3.o3,alpha = 0.8, label= 'o3')
    ax[1][0].plot(statoFiltrato3.date, statoFiltrato3.so2, alpha = 0.8,label= 'so2')
    ax[1][0].plot(statoFiltrato3.date, statoFiltrato3.co, alpha = 0.8,label= 'co')
    ax[1][0].set_title('filtrato f < '+ str(filtri[2])+ ' $d^{-1}$')

    ax[1][1].plot(statoFiltrato4.date, statoFiltrato4.no2,alpha = 0.8, label= 'no2')
    ax[1][1].plot(statoFiltrato4.date, statoFiltrato4.o3,alpha = 0.8, label= 'o3')
    ax[1][1].plot(statoFiltrato4.date, statoFiltrato4.so2, alpha = 0.8,label= 'so2')
    ax[1][1].plot(statoFiltrato4.date, statoFiltrato4.co,alpha = 0.8, label= 'co')
    ax[1][1].set_title('filtrato f < '+ str(filtri[3])+ ' $d^{-1}$')
      
    ax[0][0].set_xlabel('Tempo [d]')
    ax[0][0].set_ylabel('Concentrazione media [ppm]')
    ax[0][1].set_xlabel('Tempo [d]')
    ax[0][1].set_ylabel('Concentrazione media [ppm]')
    ax[1][0].set_xlabel('Tempo [d]')
    ax[1][0].set_ylabel('Concentrazione media [ppm]')
    ax[1][1].set_xlabel('Tempo [d]')
    ax[1][1].set_ylabel('Concentrazione media [ppm]')

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)
    
    ax[0][0].legend()
    ax[0][1].legend()
    ax[1][0].legend()
    ax[1][1].legend()

    plt.show()


    
def graficoTuttiStati(s1,s1Name, s2, s2Name, s3,s3Name, s4, s4Name, s5, s5Name, title, filtro):
    ''' Produce un subplot con quattro grafici uno per inquinante della concentrazione nel tempo di tutti e cinque gli stati. ''' 
    fig,ax = plt.subplots(2,2, figsize = (18,12))
    fig.suptitle(title)

    ax[0][0].plot(s1.date, s1.no2, alpha = 0.8, label= s1Name)
    ax[0][0].plot(s2.date, s2.no2, alpha = 0.8, label= s2Name)
    ax[0][0].plot(s3.date, s3.no2,alpha = 0.8, label= s3Name)
    ax[0][0].plot(s4.date, s4.no2, alpha = 0.8,label= s4Name)
    ax[0][0].plot(s5.date, s5.no2, alpha = 0.8,label= s5Name)
    
    ax[0][1].plot(s1.date, s1.o3,alpha = 0.8, label= s1Name)
    ax[0][1].plot(s2.date, s2.o3,alpha = 0.8, label= s2Name)
    ax[0][1].plot(s3.date, s3.o3,alpha = 0.8, label= s3Name)
    ax[0][1].plot(s4.date, s4.o3,alpha = 0.8, label= s4Name)
    ax[0][1].plot(s5.date, s5.o3, alpha = 0.8,label= s5Name)

    ax[1][0].plot(s1.date, s1.so2,alpha = 0.8, label= s1Name)
    ax[1][0].plot(s2.date, s2.so2,alpha = 0.8, label= s2Name)
    ax[1][0].plot(s3.date, s3.so2,alpha = 0.8, label= s3Name)
    ax[1][0].plot(s4.date, s4.so2,alpha = 0.8, label= s4Name)
    ax[1][0].plot(s5.date, s5.so2,alpha = 0.8, label= s5Name)

    ax[1][1].plot(s1.date, s1.co,alpha = 0.8, label= s1Name)
    ax[1][1].plot(s2.date, s2.co,alpha = 0.8, label= s2Name)
    ax[1][1].plot(s3.date, s3.co,alpha = 0.8, label= s3Name)
    ax[1][1].plot(s4.date, s4.co,alpha = 0.8, label= s4Name)
    ax[1][1].plot(s5.date, s5.co,alpha = 0.8, label= s5Name)

    ax[0][0].set_xlabel('Tempo [d]')
    ax[0][0].set_ylabel('NO2 [ppm]')
    ax[0][1].set_xlabel('Tempo [d]')
    ax[0][1].set_ylabel('O3 [ppm]')
    ax[1][0].set_xlabel('Tempo [d]')
    ax[1][0].set_ylabel('SO2 [ppm]')
    ax[1][1].set_xlabel('Tempo [d]')
    ax[1][1].set_ylabel('CO [ppm]')

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

    currentDirectory = os.getcwd()
    if filtro == '':
        plt.savefig(currentDirectory +'/datiSalvati/analisiStati/confrontoStati/inqStati.png')
    else:
        plt.savefig(currentDirectory +'/datiSalvati/analisiStati/confrontoStati/inqStatiFiltro' +filtro+'.png')
        
    plt.show()

#---------------------------------------------------------------#
#              Definizione moduli grafici Rumore                #
#---------------------------------------------------------------#

def graficoRumore(diff, p1, p2, p3, p4, mask, title, filtro, name):
    '''
    Produce un subplot di quattro grafici della concentrazione media degli inquinanti in funzione del tempo, in ogni grafico è riportato il dato originale e quello filtrato.  
    Salva la figura all'interno della cartella corrispondente allo stato all'interno di datiSalvati/analisiStati.
    Parametri:
    stato: di tipo classe Stato, contiene dati originali
    statoFiltrato: di tipo classe Stato, contiene i dati filtrati
    title: stringa, titolo del grafico
    name: stringa, nome dello stato
    filtro: reale, frequenza di filtro
    scale: stringa, se scale = 'log' i grafici sono in scala logaritminca
    '''
    fig,ax = plt.subplots(2,2, figsize = (18,12))
    fig.suptitle(title)
    
    ax[0][0].plot(diff.no2F[mask[0]], diff.no2P[mask[0]])
    ax[0][0].plot(diff.no2F[mask[0]], fz.rumore(diff.no2F[mask[0]], p1[0], p1[1]))
    ax[0][1].plot(diff.o3F[mask[1]], diff.o3P[mask[1]])
    ax[0][1].plot(diff.o3F[mask[1]], fz.rumore(diff.o3F[mask[1]],  p2[0], p2[1]))
    ax[1][0].plot(diff.so2F[mask[2]], diff.so2P[mask[2]])
    ax[1][0].plot(diff.so2F[mask[2]], fz.rumore(diff.so2F[mask[2]],  p3[0], p3[1]))
    ax[1][1].plot(diff.coF[mask[3]], diff.coP[mask[3]])
    ax[1][1].plot(diff.coF[mask[3]], fz.rumore(diff.coF[mask[3]],  p4[0], p4[1]))

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)
    
    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()

    ax[0][0].set_xlabel('Tempo [d]')
    ax[0][0].set_ylabel('Concentrazione media NO2 [ppm]')
    ax[0][1].set_xlabel('Tempo [d]')
    ax[0][1].set_ylabel('Concentrazione media O3 [ppm]')
    ax[1][0].set_xlabel('Tempo [d]')
    ax[1][0].set_ylabel('Concentrazione media SO2 [ppm]')
    ax[1][1].set_xlabel('Tempo [d]')
    ax[1][1].set_ylabel('Concentrazione media CO [ppm]')
    
    ax[0][0].set_xscale('log')
    ax[0][1].set_xscale('log')
    ax[1][0].set_xscale('log')
    ax[1][1].set_xscale('log')
    ax[0][0].set_yscale('log')
    ax[0][1].set_yscale('log')
    ax[1][0].set_yscale('log')
    ax[1][1].set_yscale('log')

    currentDirectory = os.getcwd()
    plt.savefig(currentDirectory +'/datiSalvati/analisiStati/' +  name + '/fitRumoreFiltro' + str(filtro) + name + '.png')
    plt.show()

#---------------------------------------------------------------#
#       Definizione moduli grafici per analisi Stazioni         #
#---------------------------------------------------------------#

def subplotInquinanti(stato, title, name):
    
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    for i in range(len(stato.siteNum)):
        ax[0][0].plot(stato.sites[i].date, stato.sites[i].no2, label = 'site num ' + str(stato.siteNum[i]), alpha = 0.6)
        ax[0][1].plot(stato.sites[i].date, stato.sites[i].o3, alpha = 0.6)
        ax[1][0].plot(stato.sites[i].date, stato.sites[i].so2, alpha = 0.6)
        ax[1][1].plot(stato.sites[i].date, stato.sites[i].co, alpha = 0.6)

    ax[0][0].set_xlabel('Tempo [d]')
    ax[0][0].set_ylabel('Concentazione media NO2 [ppm]')
    ax[0][1].set_xlabel('Tempo [d]')
    ax[0][1].set_ylabel('Concentrazione media O3 [ppm]')
    ax[1][0].set_xlabel('Tempo [d]')
    ax[1][0].set_ylabel('Concentrazione media SO2 [ppm]')
    ax[1][1].set_xlabel('Tempo [d]')
    ax[1][1].set_ylabel('Concentrazione media CO [ppm]')

    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)

    fig.legend()
    currentDirectory = os.getcwd()
    plt.savefig(currentDirectory +'/datiSalvati/analisiStazioni/' + name + '/inqSt'+name+'.png')
    plt.show()


def subplotInquinantiFft(stato, title, scale, name):
    
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    for i in range(len(stato.siteNumFft)):
        ax[0][0].plot(stato.sitesFft[i].no2F[1:], stato.sitesFft[i].no2P[1:], label = 'site num ' + str(stato.siteNumFft[i]), alpha = 0.7)
        ax[0][1].plot(stato.sitesFft[i].o3F[1:], stato.sitesFft[i].o3P[1:], alpha = 0.7)
        ax[1][0].plot(stato.sitesFft[i].so2F[1:], stato.sitesFft[i].so2P[1:], alpha = 0.7)
        ax[1][1].plot(stato.sitesFft[i].coF[1:], stato.sitesFft[i].coP[1:], alpha = 0.7)

    ax[0][0].set_xlabel('Frequenza [1/d]')
    ax[0][0].set_ylabel('Spettro di potenza NO2')
    ax[0][1].set_xlabel('Frequenza [1/d]')
    ax[0][1].set_ylabel('Spettro di potenza O3')
    ax[1][0].set_xlabel('Frequenza [1/d]')
    ax[1][0].set_ylabel('Spettro di potenza SO2')
    ax[1][1].set_xlabel('Frequenza [1/d]')
    ax[1][1].set_ylabel('Spettro di potenza CO')

    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()

    if scale == 'log':
        ax[0][0].set_xscale('log')
        ax[0][0].set_yscale('log')
        ax[0][1].set_xscale('log')
        ax[0][1].set_yscale('log')
        ax[1][1].set_xscale('log')
        ax[1][1].set_yscale('log')
        ax[1][0].set_xscale('log')
        ax[1][0].set_yscale('log')
        
    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)

    fig.legend()
    if scale == 'log':
        currentDirectory = os.getcwd()
        plt.savefig(currentDirectory +'/datiSalvati/analisiStazioni/' + name + '/spPotFreq'+name+'Log.png')
    else:
        currentDirectory = os.getcwd()
        plt.savefig(currentDirectory +'/datiSalvati/analisiStazioni/' + name + '/spPotFreq'+name+'.png')
    plt.show()


def subplotInquinantiFftPeriodo(stato, title, scale, name):
    
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    for i in range(len(stato.siteNumFft)):
        ax[0][0].plot(1/stato.sitesFft[i].no2F[1:], stato.sitesFft[i].no2P[1:], label = 'site num ' + str(stato.siteNumFft[i]), alpha = 0.7)
        ax[0][1].plot(1/stato.sitesFft[i].o3F[1:], stato.sitesFft[i].o3P[1:], alpha = 0.7)
        ax[1][0].plot(1/stato.sitesFft[i].so2F[1:], stato.sitesFft[i].so2P[1:], alpha = 0.7)
        ax[1][1].plot(1/stato.sitesFft[i].coF[1:], stato.sitesFft[i].coP[1:], alpha = 0.7)

    ax[0][0].set_xlabel('Periodo [d]')
    ax[0][0].set_ylabel('Spettro di potenza NO2')
    ax[0][1].set_xlabel('Periodo [d]')
    ax[0][1].set_ylabel('Spettro di potenza O3')
    ax[1][0].set_xlabel('Periodo [d]')
    ax[1][0].set_ylabel('Spettro di potenza SO2')
    ax[1][1].set_xlabel('Periodo [d]')
    ax[1][1].set_ylabel('Spettro di potenza CO')

    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()

    ax[0][0].xaxis.set_tick_params(labelsize=7)
    ax[0][1].xaxis.set_tick_params(labelsize=7)
    ax[1][0].xaxis.set_tick_params(labelsize=7)
    ax[1][1].xaxis.set_tick_params(labelsize=7)

    if scale == 'log':
        ax[0][0].set_xscale('log')
        ax[0][0].set_yscale('log')
        ax[0][1].set_xscale('log')
        ax[0][1].set_yscale('log')
        ax[1][1].set_xscale('log')
        ax[1][1].set_yscale('log')
        ax[1][0].set_xscale('log')
        ax[1][0].set_yscale('log')

    fig.legend()
    
    if scale == 'log':
        currentDirectory = os.getcwd()
        plt.savefig(currentDirectory +'/datiSalvati/analisiStazioni/' + name + '/spPotPer'+name+'Log.png')
    else:
        currentDirectory = os.getcwd()
        plt.savefig(currentDirectory +'/datiSalvati/analisiStazioni/' + name + '/spPotPer'+name+'.png')
    plt.show()
    plt.show()




    
