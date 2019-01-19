import numpy as np
import matplotlib.pyplot as plt

r = .25 # growth rate / yr
K = 100 # carrying capacity
t = 40 # number of years
inicial = 1

num = np.zeros(t+1)

num[0] = inicial
for i in range(t):
    num[i+1] = num[i] + r*num[i] * (1 - num[i] / K)

plt.plot(range(t+1),num, 'b')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Crecimiento logistico')
plt.axvline(np.argmax(np.diff(num)),  color = 'k'  )
print(num)
plt.show()

