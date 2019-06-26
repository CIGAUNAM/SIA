import numpy as np
import matplotlib.pyplot as plt

r = .25 # growth rate / yr
K = 100 # carrying capacity
t = 400 # number of years
num = np.zeros(t+1)
num[0] = 1
for i in range(t):
    num[i+1] = num[i]+r*num[i]*(1-num[i]/K)
    num[i+1] = num[i]+r*num[i]*(1-num[i]/K)
plt.plot(range(t+1),num, 'b')
plt.xlabel('Tiempo')
plt.ylabel('Individuos')
plt.title('tasa de crecimiento: ' + str(r) + ' Capacidad de carga:' + str(K))
plt.show()