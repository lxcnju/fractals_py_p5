# fractals_py_p5
Five methods to draw beautiful pictures and curves which are called fractals.

* 代码架构
* 原理解析
  * 分形介绍
  * Escape Time Fractals
  * L-system
  * Iterated Function Systems
  * Attractor
  * Random Fractals

## 代码架构
 * draw_mandelbrot.py  绘制Mandelbrot分形
 * draw_julia.py  绘制Julia分形
 * draw_lsystem.py  绘制L-system分形
 * draw_hilbert.py  绘制hilbert曲线
 * draw_dragon.py  绘制龙形曲线
 * draw_lorenz.py  绘制洛伦兹吸引子
 * peter_de_jonge_attractor.js  绘制peter de jonge吸引子
 * dla.js  Diffusion Limited Aggregation随机游走

## 原理解析
  * 分形介绍 <br>
  [Fractals](https://en.wikipedia.org/wiki/Fractal)指的是一些具有自相似的形状，放大局部之后会产生和整体很相似的形状，这种现象在自然界里面很常见，比如雪花图案、树叶脉络、石头纹理、山脉、珊瑚树等等。数学家曼德布罗特(B. B. Mandelbrot)经历了不平凡的潜心研究，于1975年出版了他的关于分形几何的专著《分形、机遇和维数》，标志着分形理论的诞生。分形具有一些特点：整体上看是不规则的，但是局部和整体具有相似性。如何利用计算机绘制出这些分形图案则是本项目的主要出发点，一般来说有五种方法绘制，下面分别介绍。
  * Escape Time Fractals <br>
      * 介绍 <br>
      在空间的一个点，比如二维平面(x,y)点，利用一系列方程进行迭代，根据一些迭代信息(比如达到收敛的迭代次数)进行设置该点的像素点。常见的有Mandelbrot，Julia，Lyapunov等等。
      * Mandelbrot Set <br>
      Mandelbrot分形是利用方程Z = Z * Z + C在复数平面上进行迭代，复数平面上Z = x + iy，C = a + ib。主要思想如下：(1)构建一个像素点矩阵Array，大小为m * n；(2)对于每一个像素点(p, q)，初始化a和b，比如a = amin + p * (amax - amin)/m，b = bmin + q * (bmax - bmin)/n；(3)设置初始迭代点Z = (0, 0)，然后根据Z = Z * Z + C进行迭代，其中C = a + ib，当|Z|收敛时，或者|Z|不收敛达到最大阈值时，记录迭代次数K，Array(p,q)=K。<br>
      通过以上思想则完成了Mandelbrot分形的绘制，其中m,n决定了图形大小，amin,amax,bmin,bmax是一些参数，不同的设置会得到不同的图形。<br>
      ![Mandelbrot示例]()
      * Julia Set <br>
      和Mandelbrot分形相同的是，Julia也是利用方程Z = Z * Z + C在复数平面上进行迭代，复数平面上Z = x + iy，C = a + ib。但是其主要思想如下：(1)构建一个像素点矩阵Array，大小为m * n；(2)对于每一个像素点(p, q)，初始化x和y，比如x0 = xmin + p * (xmax - xmin)/m，y0 = ymin + q * (ymax - ymin)/n；(3)设置初始迭代点Z = (x0, y0)，然后根据Z = Z * Z + C进行迭代，其中C = a + ib，当|Z|收敛时，或者|Z|不收敛达到最大阈值时，记录迭代次数K，Array(p,q)=K。<br>
      通过以上思想则完成了Julia分形的绘制，其中m,n决定了图形大小，ymin,ymax,ymin,ymax是一些参数，决定了每个像素点的初始迭代坐标，a,b也是参数，不同的参数设置会产生不同的图形。<br>
      这里可以看出和Mandelbrot不同的是，Julia每个像素点迭代时初始迭代点Z不一样，但是常数C一样；而Mandelbrot里面是初始迭代点都为(0,0)，但是常数C不一样，由像素点矩阵位置决定。<br>
      ![Julia示例]()
  * L-system <br>
      * 介绍 <br>
      L-system是利用字符串来代表图形绘制的规则，字符串里面有一些符号，主要包括两种：(1)替换规则字符，比如大写字母"A"、"B"等等，每个字母代表了一个字符串，在下一次迭代的时候进行替换；(2)动作规则字符，比如"+"、"-"、"\["，以及部分大写字母"F"等等，代表在绘图时执行某些动作。<br>
      * 举例 gosper曲线 <br>
      Gosper曲线的规则集如下：rules = {"start": "A", "reps": {"A": "A-B--B+A++AA+B-", "B": "+A-BB--B-A++A+B"}, "level": 4, "rotate": np.pi / 3, "actions": {"+": "left", "-": "right", "A": "forward", "B": "forward"}}。 <br>
      level是指的迭代次数，假如level=1，则返回的字符串是"A"，而A在actions里面代表向前走一步，反映到图形上则是绘制一条线段；假如level=2，利用reps里面替换规则进行替换"A"，得到"A-B--B+A++AA+B-"，然后再把字符串里面的B全部利用"+A-BB--B-A++A+B"进行替换得到"A-+A-BB--B-A++A+B--+A-BB--B-A++A+B+A++AA++A-BB--B-A++A+B-"，代表的规则是：先向前绘制一条线段，然后右旋rotate角度，再左旋rotate角度，绘制一条线段，右旋rotate角度，绘制一条线段，绘制一条线段... <br>
      所以，L-system可以将复杂图形的绘制转变为字符串的替换和一系列动作的执行，从而实现起来比较容易。<br>
      ![L-system示例]()
  * Iterated Function Systems <br>
      * 介绍 <br>
      这个和L-system很像，是使用函数进行递归调用，从而产生一系列迭代的点，产生具有规则性的图形，一般来说通过迭代函数系统生成的图形都具有空间填充的能力，比如hilbert、koch曲线等等。<br>
      * Hilbert曲线 <br>
      Hilbert曲线是
      * Dragon曲线 <br>
  * Attractor
  * Random Fractals
  
 

