import numpy as np
import statsmodels.api as sm
import pylab
import pandas as pd
import matplotlib.pyplot as plt

#column_names = ['X', 'Y', 'pH', 'Ca']
#csv = pd.read_csv('phCa.csv', names = column_names)
csv = pd.read_csv('ej_bivar.csv')
#print(csv['pH'])
print(csv)
#sm.qqplot(test, line='45')
plt.scatter(csv['tamano'], csv['kilometraje'])
plt.plot(csv["tamano"].mean(), csv["kilometraje"].mean(), "or")
plt.show()
pylab.show()
print()
#print(np.cov(np.stack(np.array(csv))))

print(csv.cov())
#-168.6
#print(np.var(csv))



