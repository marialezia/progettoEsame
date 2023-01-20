import pandas as pd
import numpy as np
import classi as cl
import sys, os
from tqdm import tqdm
import matplotlib.pyplot as plt

def subplotInquinanti(stato, indice):
    fig,ax = plt.subplots(2,2, figsize = (24,6))

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

def subplots(stato, sitesNum):
    for i in range(len(sitesNum)):
        subplotInquinanti(stato, i)
