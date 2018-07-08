#-*- coding:utf-8 -*-
'''
  绘制mandelbrot集合
  Z = Z * Z + C
  构造一个像素点矩阵，每个灰度级利用上诉公式进行迭代，常数C是通过pn,qn决定，然后满足一定条件后停止迭代，迭代次数作为像素点的像素值
'''

import numpy as np
from matplotlib import pyplot as plt

def draw_mandelbrot(init_point = [0.0, 0.0], 
                    pmin = 0.382,
                    pmax = 0.418,
                    qmin = -0.16,
                    qmax = -0.14,
                    M = 100,
                    level = 128,
                    x_reso = 800,
                    y_reso = 800):
    # pmin pmax qmin qmax 决定了迭代过程常数值，是要调的参数
    # M是停止条件之一
    # level是最大迭代次数，即最大灰度级
    # x_reso y_reso决定了图像大小
    delta_p = (pmax - pmin) / x_reso
    delta_q = (qmax - qmin) / y_reso
    points = np.zeros([x_reso + 1, y_reso + 1])
    
    for i in range(x_reso + 1):
        for j in range(y_reso + 1):
            pn = pmin + (i - 1) * delta_p     # 常数项
            qn = qmin + (j - 1) * delta_q
            n = 0
            x = init_point[0]
            y = init_point[1]
            while x * x + y * y < M * M and n < level:
                temp = x
                x = x * x - y * y + pn        # 迭代
                y = 2 * temp * y + qn
                n += 1                        # 迭代次数
            points[i, j] = n                  # 设置像素点值
    plt.figure()
    plt.imshow(points)
    plt.show()
    
def main():
    for k in range(10):
        pmin = 2 * np.random.rand() - 1
        pmax = 2 * np.random.rand() - 1
        if pmax < pmin:
            (pmin, pmax) = (pmax, pmin)
        qmin = 2 * np.random.rand() - 1
        qmax = 2 * np.random.rand() - 1
        if qmax < qmin:
            (qmin, qmax) = (qmax, qmin)
        print(pmin, pmax, qmin, qmax)
        draw_mandelbrot(pmin = pmin, pmax = pmax, qmin = qmin, qmax = qmax)

main()