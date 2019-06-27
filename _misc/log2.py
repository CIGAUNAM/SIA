import numpy as np
import matplotlib.pyplot as plt

r = 2 # growth rate / yr
K = 5000 # carrying capacity
t = 40 # number of years



xnum = [0]
ynum = [300]

c = 0

while c < 20:
    xnum.append(xnum[-1] + 1)
    ynum.append(int(r*(((K-ynum[-1])/K)*ynum[-1])))
    c += 1


plt.plot(xnum,ynum, 'b')
print(xnum)
print(ynum)

plt.xlabel('Tiempo')
plt.ylabel('Individuos')
plt.title('tasa de crecimiento: ' + str(r))
plt.show()