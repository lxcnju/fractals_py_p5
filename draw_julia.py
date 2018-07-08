#-*- coding:utf-8 -*-
'''
  绘制Julia集合
  Z = Z * Z + C
  同样构建像素点矩阵
  不同于Mandelbrot，这里每个像素点的迭代初始点不同，常数项相同
'''

import numpy as np
from matplotlib import pyplot as plt

def draw_julia(xmin = -0.5,
               xmax = 0.5,
               ymin = -0.5,
               ymax = 0.5,
               M = 100,
               level = 128,
               x_reso = 800,
               y_reso = 600,
               pn = 0.1,
               qn = 0.1):
    # xmin xmax ymin ymax 决定了迭代过程Z的初始值
    # M是停止条件之一
    # level是最大迭代次数，即最大灰度级
    # x_reso y_reso决定了图像大小
    # pn qn是常数项
    delta_x = (xmax - xmin) / x_reso
    delta_y = (ymax - ymin) / y_reso
    points = np.zeros([x_reso + 1, y_reso + 1])
    
    for i in range(x_reso + 1):
        for j in range(y_reso + 1):
            n = 0
            x = xmin + (i - 1) * delta_x      # 迭代初始值
            y = ymin + (j - 1) * delta_y
            while x * x + y * y < M * M and n < level:
                temp = x
                x = x * x - y * y + pn        # 迭代
                y = 2 * temp * y + qn
                n += 1
            points[i, j] = n                  # 像素点
    plt.figure()
    plt.imshow(points)
    plt.show()
    
def main():
    for k in range(5):
        pn = 2 * np.random.rand() - 1
        qn = 2 * np.random.rand() - 1
        print(pn, qn)
        draw_julia(pn = pn, qn = qn)
    draw_julia(pn = 0.194, qn = 0.6557)
main()