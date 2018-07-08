#-*- coding:utf-8 -*-
'''
  绘制龙形曲线
'''

import numpy as np
from matplotlib import pyplot as plt

def generate_dragon(level, alpha = np.pi / 4):
    if level == 0:
        return [[0.0, 0.0], [10.0, 10.0]]
    sub_points = generate_dragon(level - 1)  # 获得level-1的点
    cos_alp = np.cos(alpha)
    sin_alp = np.sin(alpha)
    new_points = []                          # 新的数据点
    for i in range(len(sub_points) - 1):
        x1 = sub_points[i][0]
        y1 = sub_points[i][1]
        x2 = sub_points[i + 1][0]
        y2 = sub_points[i + 1][1]    
        if i % 2 == 0:
            new_x = 0.707 * (cos_alp * (x2 - x1) + sin_alp * (y2 - y1)) + x1
            new_y = 0.707 * (-sin_alp * (x2 - x1) + cos_alp * (y2 - y1)) + y1
        else:
            new_x = 0.707 * (cos_alp * (x2 - x1) - sin_alp * (y2 - y1)) + x1
            new_y = 0.707 * (sin_alp * (x2 - x1) + cos_alp * (y2 - y1)) + y1
        new_points.append([x1, y1])
        new_points.append([new_x, new_y])
    new_points.append([x2, y2])
    return new_points
        
def draw_dragon(level = 10):
    points = generate_dragon(level)
    
    x_list = [p[0] for p in points]
    y_list = [p[1] for p in points]
    
    plt.plot(x_list, y_list, 'y-')
    plt.show()

def main():
    draw_dragon(level = 1)
    draw_dragon(level = 2)
    draw_dragon(level = 3)
    draw_dragon(level = 4)
    draw_dragon(level = 5)
    draw_dragon(level = 6)
    draw_dragon(level = 7)
    draw_dragon(level = 8)
    draw_dragon(level = 9)
    draw_dragon(level = 10)
    draw_dragon(level = 11)
    draw_dragon(level = 12)
    draw_dragon(level = 13)

main()
    