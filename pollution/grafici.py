import pandas as pd
import numpy as np
import classi as cl
import sys, os
from tqdm import tqdm
import matplotlib.pyplot as plt

def plotInquinanti(stato, indice, title):
    plt.title(title)
    plt.errorbar(stato.sites[indice].date, stato.sites[indice].no2, yerr= stato.sites[indice].no2Err, label= 'NO2')
    plt.errorbar(stato.sites[indice].date, stato.sites[indice].o3, yerr= stato.sites[indice].o3Err, label = 'O3')
    plt.errorbar(stato.sites[indice].date, stato.sites[indice].so2, yerr= stato.sites[indice].so2Err, label = 'SO2')
    plt.errorbar(stato.sites[indice].date, stato.sites[indice].co, yerr= stato.sites[indice].coErr, label = 'CO')
    plt.grid()
    plt.xlabel('Time')
    plt.ylabel('concentrazione')
    plt.legend()
    plt.show()

def plot(stato):
    for i in range(len(stato.siteNum)):
        plotInquinanti(stato, i, 'Stazione di monitoraggio numero ' + str(stato.siteNum[i]))

def plotInquinanti2(stato):
    plt.plot(stato.date, stato.no2,label= 'NO2')
    plt.plot(stato.date, stato.o3, label = 'O3')
    plt.plot(stato.date, stato.so2, label = 'SO2')
    plt.plot(stato.date, stato.co,  label = 'CO')
    plt.grid()
    plt.xlabel('Time')
    plt.ylabel('concentrazione')
    plt.legend()
    plt.show()

        
def subplotInquinanti(stato, indice, title):
    fig,ax = plt.subplots(2,2, figsize = (24,6))
    fig.suptitle(title)

    ax[0][0].errorbar(stato.sites[indice].date, stato.sites[indice].no2, yerr= stato.sites[indice].no2Err)
    ax[0][1].errorbar(stato.sites[indice].date, stato.sites[indice].o3, yerr= stato.sites[indice].o3Err)
    ax[1][0].errorbar(stato.sites[indice].date, stato.sites[indice].so2, yerr= stato.sites[indice].so2Err)
    ax[1][1].errorbar(stato.sites[indice].date, stato.sites[indice].co, yerr= stato.sites[indice].coErr)

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

    plt.show()

def subplots(stato):
    for i in range(len(stato.siteNum)):
        subplotInquinanti(stato, i, 'Stazione di monitoraggio numero ' + str(stato.siteNum[i]))


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

def plotFft2(stato):
    lNo2 = len(stato.no2F)//2
    lO3 = len(stato.o3F)//2
    lSo2 = len(stato.so2F)//2
    lCo = len(stato.coF)//2

    plt.plot(stato.no2F[lNo2+1:], stato.no2P[lNo2+1:], label = 'NO2')
    plt.plot(stato.o3F[lO3+1:], stato.o3P[lO3+1:], label = 'O3')
    plt.plot(stato.so2F[lSo2+1:], stato.so2P[lSo2+1:], label = 'SO2')
    plt.plot(stato.coF[lCo+1:], stato.coP[lCo+1:], label = 'CO')
    plt.grid()
    plt.xlabel('frequenza')
    plt.legend()
    plt.show()
