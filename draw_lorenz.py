# -*- coding: utf-8 -*-

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

xs, ys, zs = [], [], []
def mkPoints():
    a, b, c = 10.0, 28.0, 8.0 / 3.0
    h = 0.01
    x0, y0, z0 = 0.1, 0, 0
    for i in range(10000):
        x1 = x0 + h * a * (y0 - x0)
        y1 = y0 + h * (x0 * (b - z0) - y0)
        z1 = z0 + h * (x0 * y0 - c * z0)
        x0, y0, z0 = x1, y1, z1
        xs.append(x0)
        ys.append(y0)
        zs.append(z0)

if __name__ == "__main__":
    mpl.rcParams["legend.fontsize"] = 10
    fig = plt.figure(figsize = (8.0, 8.0))
    ax = Axes3D(fig)
    mkPoints()
    ax.plot(xs, ys, zs, label = 'Lorenz')
    #ax.legend()
    plt.axis("off")
    plt.show()