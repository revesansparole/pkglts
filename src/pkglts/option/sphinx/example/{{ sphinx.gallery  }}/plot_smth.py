"""
Example plot
============

This is just an example.
"""
from math import pi

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,100,200)
y = np.sin(x / 50 * pi)

fig, ax = plt.subplots(1, 1, figsize=(10, 6))

ax.plot(x, y)

fig.tight_layout()
plt.show()
