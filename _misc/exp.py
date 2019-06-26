import numpy as np
import matplotlib.pyplot as plt

r = 2 # growth rate / yr
t = 40 # number of years

xnum = list(range(t))
ynum = list(range(t))
ynum[0] = 0
ynum[1] = 1*r

for i in range(1, t-1):
    ynum[i+1] = ynum[i]*r

plt.plot(xnum,ynum, 'b')
print(xnum)
print(ynum)

plt.xlabel('Tiempo')
plt.ylabel('Individuos')
plt.title('tasa de crecimiento: ' + str(r))
plt.show()