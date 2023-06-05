from matplotlib import pyplot as plt
import numpy as np
t = np.arange(0.,5.,0.05)
y1 = np.sin(2*np.pi*t)

plt.plot(t,y1,'r--')
plt.show()
plt.savefig('foo.png')