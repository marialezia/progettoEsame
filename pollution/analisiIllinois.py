import numpy as np
import pandas as pd
import sys, os
import classi as cl
import funzioni as fz
import matplotlib.pyplot as plt
import grafici as gr

ilDf = pd.read_csv('newIllinois.csv')
sitesNum =([10,4002,4201])
illinois = fz.createStato(ilDf, sitesNum)

gr.subplots(illinois, sitesNum)


'''
sites = ([fz.createSite(illinois, 10), fz.createSite(illinois, 4002), fz.createSite(illinois, 4201)])
site10 = fz.createSite(illinois, 10)
site4002 = fz.createSite(illinois, 4002)

plt.plot(site4002.date, site4002.no2)
plt.show()
print(site4002.o3)
'''



