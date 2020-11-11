import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

n = 100
x = np.linspace(0,2,n)
y1 = np.sin(2*np.pi*x)
y2 = np.sin(4*np.pi*x)
y3 = np.sin(6*np.pi*x)

df = pd.DataFrame(np.c_[y1, y2, y3], index=x)

ax = sns.lineplot(data=df)
plt.show()