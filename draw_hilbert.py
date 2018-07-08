#-*- coding:utf-8 -*-
'''
  绘制Hilbert曲线
  递归调用进行绘制
'''

import numpy as np
from matplotlib import pyplot as plt

def generate_hilbert(level, direction, alpha, x, y):
    '''
      level 递归调用层次
      direction 方向
      alpha 角度
      x x坐标列表
      y y坐标列表
    '''
    if level == 0:
        return
    generate_hilbert(level - 1, direction - alpha, -alpha, x, y) # 递归
    x.append(x[-1] + np.cos(direction))                          # 加上边界连线
    y.append(y[-1] + np.sin(direction))
    
    generate_hilbert(level - 1, direction, alpha, x, y)
    x.append(x[-1] + np.cos(direction - alpha))
    y.append(y[-1] + np.sin(direction - alpha))
    
    generate_hilbert(level - 1, direction, alpha, x, y)
    x.append(x[-1] + np.cos(direction - 2 * alpha))
    y.append(y[-1] + np.sin(direction - 2 * alpha))
    
    generate_hilbert(level - 1, direction + alpha, -alpha, x, y)

def draw_hilbert(level):
    x = [0.0]
    y = [0.0]
    generate_hilbert(level = level, direction = np.pi / 2, alpha = np.pi / 2, x = x, y = y)
    plt.figure()
    plt.plot(x, y)
    plt.show()

def main():
    draw_hilbert(level = 1)
    draw_hilbert(level = 2)
    draw_hilbert(level = 3)
    draw_hilbert(level = 4)
    draw_hilbert(level = 5)
    draw_hilbert(level = 6)
main()