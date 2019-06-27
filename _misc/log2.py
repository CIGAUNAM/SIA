import numpy as np
import matplotlib.pyplot as plt

r = 1.15 # growth rate / yr
K = 10 # carrying capacity
t = 40 # number of years

xnum = list(range(t))
ynum = list(range(t))
ynum[0] = 0
ynum[1] = r*((K-1/K))

for i in range(1, t-1):
    ynum[i+1] = r*((K-ynum[i]/K))*ynum[i]

plt.plot(xnum,ynum, 'b')
print(xnum)
print(ynum)

plt.xlabel('Tiempo')
plt.ylabel('Individuos')
plt.title('tasa de crecimiento: ' + str(r) + ' Capacidad de carga:' + str(K))
plt.show()