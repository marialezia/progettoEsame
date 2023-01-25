import pandas as pd
import numpy as np
import classiStazioni as clSz
import sys, os
from tqdm import tqdm
import matplotlib.pyplot as plt
    
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


'''
def plotInquinanti(stato, indice, title):
    plt.figure(figsize = (12,12))
    plt.title(title)
    plt.plot(stato.sites[indice].date, stato.sites[indice].no2,label= 'NO2')
    plt.plot(stato.sites[indice].date, stato.sites[indice].o3, label = 'O3')
    plt.plot(stato.sites[indice].date, stato.sites[indice].so2, label = 'SO2')
    plt.plot(stato.sites[indice].date, stato.sites[indice].co,  label = 'CO')
    plt.grid()
    plt.xlabel('Time', size = 10)
    plt.ylabel('concentrazione')
    plt.legend()
    plt.show()


def plot(stato):
    for i in range(len(stato.siteNum)):
        plotInquinanti(stato, i, 'Stazione di monitoraggio numero ' + str(stato.siteNum[i]))

    
def subplots(stato):
    for i in range(len(stato.siteNum)):
        subplotInquinanti(stato, i)


def subplotStazioni(stato, title):
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    for i in range(len(stato.siteNum)):       
            ax[0][0].errorbar(stato.sites[i].date, stato.sites[i].no2, yerr= stato.sites[i].no2Err, label = 'stazione monitoraggio ' + str(stato.siteNum[i]))
            ax[0][1].errorbar(stato.sites[i].date, stato.sites[i].o3, yerr= stato.sites[i].o3Err, label = 'stazione monitoraggio ' + str(stato.siteNum[i]))
            ax[1][0].errorbar(stato.sites[i].date, stato.sites[i].so2, yerr= stato.sites[i].so2Err, label = 'stazione monitoraggio ' + str(stato.siteNum[i]))
            ax[1][1].errorbar(stato.sites[i].date, stato.sites[i].co, yerr= stato.sites[i].coErr, label = 'stazione monitoraggio ' + str(stato.siteNum[i]))

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

    ax[0][0].legend()
    ax[0][1].legend()
    ax[1][0].legend()
    ax[1][1].legend()
    plt.show()


def subplotInquinantiFft(stato, indice, title):
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    lNo2 = len(stato.sitesFft[indice].no2F)//2
    lO3 = len(stato.sitesFft[indice].o3F)//2
    lSo2 = len(stato.sitesFft[indice].no2F)//2
    lCo = len(stato.sitesFft[indice].coF)//2

    print(len(stato.sitesFft[indice].no2P))
    print(lNo2)
    print(len(stato.sitesFft[indice].no2P[lNo2:]))

    ax[0][0].plot(stato.sitesFft[indice].no2F[1+lNo2:], stato.sitesFft[indice].no2P[1+lNo2:])
    ax[0][1].plot(stato.sitesFft[indice].o3F[1+lO3:], stato.sitesFft[indice].o3P[1+lO3:])
    ax[1][0].plot(stato.sitesFft[indice].so2F[1+lCo:], stato.sitesFft[indice].so2P[1+lSo2:])
    ax[1][1].plot(stato.sitesFft[indice].coF[1+lCo:], stato.sitesFft[indice].coP[1+lSo2:])

    ax[0][0].set_xlabel('Freq')
    ax[0][0].set_ylabel('NO2')
    ax[0][1].set_xlabel('Freq')
    ax[0][1].set_ylabel('O3')
    ax[1][0].set_xlabel('Freq')
    ax[1][0].set_ylabel('SO2')
    ax[1][1].set_xlabel('Freq')
    ax[1][1].set_ylabel('CO')

    ax[0][0].grid()
    ax[0][1].grid()
    ax[1][0].grid()
    ax[1][1].grid()
   

    plt.show()

def subplotsFft(stato):
    for i in range(len(stato.siteNumFft)):
        subplotInquinantiFft(stato, i, 'Stazione di monitoraggio numero ' + str(stato.siteNumFft[i]))
'''
