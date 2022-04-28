import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


hist = np.zeros(100)
for row in pd.read_csv("hist.csv").values:
    hist[row[0]] = row[1]

print(sum(hist))

fig, ax = plt.subplots()

ax.set_title("File number (log) by sizes")

ax.set_ylabel("Number of files (log)")
ax.set_yscale("log")

plt.bar(np.arange(0, 100), hist)
plt.show()
