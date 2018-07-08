#-*- coding:utf-8 -*-
'''
  绘制L-System曲线
  根据设定的迭代规则（字符串替换），得到曲线字符串
  然后逐步绘制
'''

import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation

'''
  曲线规则：
    start   开始迭代的字符串
    reps    替换规则
    level   迭代次数
    rotate  旋转角度
    actions 动作规则
      left    左旋
      right   右旋
      forward 前进
      [       当前点压栈
      ]       出栈
'''

'''
# gosper
rules = {
  "start": "A",
  "reps": {"A": "A-B--B+A++AA+B-", "B": "+A-BB--B-A++A+B"},
  "level": 4,
  "rotate": np.pi / 3,
  "actions": {"+": "left", "-": "right", "A": "forward", "B": "forward"}
}
'''

'''
# Sierpinski arrowhead
rules = {
  "start": "A",
  "reps": {"A": "B-A-B", "B": "A+B+A"},
  "level": 8,
  "rotate": np.pi / 3,
  "actions": {"+": "left", "-": "right", "A": "forward", "B": "forward"}
}
'''

'''
# Hilbert
rules = {
  "start": "A",
  "reps": {"A": "-BF+AFA+FB-", "B": "+AF-BFB-FA+"},
  "level": 5,
  "rotate": np.pi / 2,
  "actions": {"+": "left", "-": "right", "F": "forward"}
}
'''

'''
# Dragon
rules = {
  "start": "FY",
  "reps": {"X": "X+YF+", "Y": "-FX-Y"},
  "level": 15,
  "rotate": np.pi / 2,
  "actions": {"+": "left", "-": "right", "F": "forward"}
}
'''

'''
rules = {
  "start": "F-F-F-F-F",
  "reps": {"F": "F-F++F+F-F-F"},
  "level": 3,
  "rotate": 72 * np.pi / 180,
  "actions": {"+": "left", "-": "right", "F": "forward"}
}
'''

'''
rules = {
  "start": "F",
  "reps": {"F": "FF[-F++F][+F--F]++F--F"},
  "level": 4,
  "rotate": 25 * np.pi / 180,
  "actions": {"+": "left", "-": "right", "F": "forward", "X" : "forward", "[" : "push", "]" : "pop"}
}
'''

'''
rules = {
  "start": "F",
  "reps": {"F": "+F[-F-X+]++F[+F-X-F]-X-F", "X" : "X-F+X"},
  "level": 4,
  "rotate": 15 * np.pi / 180,
  "actions": {"+": "left", "-": "right", "F": "forward", "X" : "forward", "[" : "push", "]" : "pop"}
}
'''

'''
# sier_qua
rules = {
  "start": "L--F--L--F",
  "reps": {"L": "+R-F-R+", "R" : "-L+F+L-"},
  "level": 10,
  "rotate": 45 * np.pi / 180,
  "actions": {"+": "left", "-": "right", "F": "forward", "[" : "push", "]" : "pop"}
}
'''

'''
# 36-72-72
rules = {
  "start": "Q",
  "reps": {"F" : "",
           "P" : "--FR++++FS--FU", 
           "Q" : "FT++FR----FS++",
           "R" : "++FP----FQ++FT",
           "S" : "FU--FP++++FQ--",
           "T" : "+FU--FP+",
           "U" : "-FQ++FT-"},
  "level": 7,
  "rotate": 36 * np.pi / 180,
  "actions": {"+": "left", "-": "right", "F": "forward", "[" : "push", "]" : "pop"}
}
'''

'''
# koch
rules = {
  "start": "F--F--F",
  "reps": {"F" : "F+F--F+F"},
  "level": 8,
  "rotate": 60 * np.pi / 180,
  "actions": {"+": "left", "-": "right", "F": "forward", "[" : "push", "]" : "pop"}
}
'''

# 32段岛屿
rules = {
  "start": "A-A-A-A",
  "reps": {"A" : "-A+A-A-A+A+AA-A+A+AA+A-A-AA+AA-AA+A+A-AA-A-A+AA-A-A+A+A-A+"},
  "level": 2,
  "rotate": 90 * np.pi / 180,
  "actions": {"+": "left", "-": "right", "A": "forward", "[" : "push", "]" : "pop"}
}


# 解析字符串
def parse_string(level):
    '''
      根据迭代次数进行替换字符串
      level为0的话则返回start
    '''
    if level == 0:
        return rules["start"]
    sub_str = parse_string(level - 1)       # 递归替换
    string = ""
    for c in sub_str:
        try:
            string += rules["reps"][c]      # 如果字符c在reps规则里面，则替换
        except KeyError:
            string += c
    return string

def generate_points(start_points, start_angle, string):
    '''
      根据字符串生成一系列点
        start_points 初始点
        start_angle  初始角度
        string       字符串规则
    '''
    points = [p for p in start_points]
    point = start_points[-1]
    angle = start_angle
    stack = []                       # 栈
    for c in string:
        if c == '+' or c == '-':
            try:
                if rules['actions'][c] == "left":
                    angle += rules['rotate']         # 左旋
                elif rules['actions'][c] == "right":
                    angle -= rules['rotate']         # 右旋
            except KeyError:
                pass
        elif c == '[' or c == ']':
            try:
                if rules['actions'][c] == 'push':
                    stack.append((point, angle))     # 入栈
                elif rules['actions'][c] == 'pop':
                    point, angle = stack[-1]         # 出栈
                    stack = stack[0:-1]
            except KeyError:
                pass
        else:
            try:
                if rules['actions'][c] == 'forward':
                    x = point[0]
                    y = point[1]
                    points.append([x + np.cos(angle), y + np.sin(angle)])  # 前进一步
                    point = points[-1]
            except KeyError:
                pass
    return points

def main():
    string = parse_string(level = rules["level"])
    points = generate_points(start_points = [[0.0, 0.0]], start_angle = 0.0, string = string)
    
    x_list = [p[0] for p in points]
    y_list = [p[1] for p in points]
    
    plt.figure(figsize = (8.0, 8.0))
    plt.plot(x_list, y_list)
    plt.show()
    
main()