import numpy as np
import matplotlib.pyplot as plt

r = 2 # growth rate / yr

xnum = [0]
ynum = [300]

while ynum[-1] < 4000:
    xnum.append(xnum[-1] + 1)
    ynum.append(ynum[-1] * r)


plt.plot(xnum,ynum, 'b')
print(xnum)
print(ynum)

plt.xlabel('Tiempo')
plt.ylabel('Individuos')
plt.title('tasa de crecimiento: ' + str(r))
plt.show()