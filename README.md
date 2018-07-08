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
      ![Mandelbrot示例](https://github.com/lxcnju/fractals_py_p5/blob/master/pics/mandelbort_2.png)
      * Julia Set <br>
      和Mandelbrot分形相同的是，Julia也是利用方程Z = Z * Z + C在复数平面上进行迭代，复数平面上Z = x + iy，C = a + ib。但是其主要思想如下：(1)构建一个像素点矩阵Array，大小为m * n；(2)对于每一个像素点(p, q)，初始化x和y，比如x0 = xmin + p * (xmax - xmin)/m，y0 = ymin + q * (ymax - ymin)/n；(3)设置初始迭代点Z = (x0, y0)，然后根据Z = Z * Z + C进行迭代，其中C = a + ib，当|Z|收敛时，或者|Z|不收敛达到最大阈值时，记录迭代次数K，Array(p,q)=K。<br>
      通过以上思想则完成了Julia分形的绘制，其中m,n决定了图形大小，ymin,ymax,ymin,ymax是一些参数，决定了每个像素点的初始迭代坐标，a,b也是参数，不同的参数设置会产生不同的图形。<br>
      这里可以看出和Mandelbrot不同的是，Julia每个像素点迭代时初始迭代点Z不一样，但是常数C一样；而Mandelbrot里面是初始迭代点都为(0,0)，但是常数C不一样，由像素点矩阵位置决定。<br>
      ![Julia示例](https://github.com/lxcnju/fractals_py_p5/blob/master/pics/julia_2.png)
  * L-system <br>
      * 介绍 <br>
      L-system是利用字符串来代表图形绘制的规则，字符串里面有一些符号，主要包括两种：(1)替换规则字符，比如大写字母"A"、"B"等等，每个字母代表了一个字符串，在下一次迭代的时候进行替换；(2)动作规则字符，比如"+"、"-"、"\["，以及部分大写字母"F"等等，代表在绘图时执行某些动作。<br>
      * 举例 gosper曲线 <br>
      Gosper曲线的规则集如下：rules = {"start": "A", "reps": {"A": "A-B--B+A++AA+B-", "B": "+A-BB--B-A++A+B"}, "level": 4, "rotate": np.pi / 3, "actions": {"+": "left", "-": "right", "A": "forward", "B": "forward"}}。 <br>
      level是指的迭代次数，假如level=1，则返回的字符串是"A"，而A在actions里面代表向前走一步，反映到图形上则是绘制一条线段；假如level=2，利用reps里面替换规则进行替换"A"，得到"A-B--B+A++AA+B-"，然后再把字符串里面的B全部利用"+A-BB--B-A++A+B"进行替换得到"A-+A-BB--B-A++A+B--+A-BB--B-A++A+B+A++AA++A-BB--B-A++A+B-"，代表的规则是：先向前绘制一条线段，然后右旋rotate角度，再左旋rotate角度，绘制一条线段，右旋rotate角度，绘制一条线段，绘制一条线段... <br>
      所以，L-system可以将复杂图形的绘制转变为字符串的替换和一系列动作的执行，从而实现起来比较容易。<br>
      ![L-system示例-Gosper](https://github.com/lxcnju/fractals_py_p5/blob/master/pics/gosper.png)
      ![L-system示例-Tree](https://github.com/lxcnju/fractals_py_p5/blob/master/pics/tree2.png)
  * Iterated Function Systems <br>
      * 介绍 <br>
      这个和L-system很像，是使用函数进行递归调用，从而产生一系列迭代的点，产生具有规则性的图形，一般来说通过迭代函数系统生成的图形都具有空间填充的能力，比如hilbert、koch曲线等等。<br>
      * Hilbert曲线 <br>
      Hilbert曲线需要进行四个分支进行递归，四个分支之间需要连接三个“连接线”，并且四个递归是有方向的递归，具体实现方式参加代码。<br>
      ![Hilbert曲线](https://github.com/lxcnju/fractals_py_p5/blob/master/pics/hilbert.png)
      * Dragon曲线 <br>
      Dragon曲线的实现需要先递归生成level-1级的点，然后对生成的点两两间生成新的点，从而得到level级的点，具体实现见代码。<br>
      ![Dragon曲线](https://github.com/lxcnju/fractals_py_p5/blob/master/pics/dragon.png)
  * Attractor
      * 介绍 <br>
      通过迭代一系列方程，通常是微分方程，或者利用某些映射来完成分形的绘制，通常称为吸引子分形曲线。Lorenz吸引子是最为常见的曲线，利用分形火焰(Fractal Flame)算法绘制的Peter De Jonge吸引子具有很强的视觉效果。<br>
      * Lorenz <br>
      洛伦兹的思想很简单，就是利用微分方程进行逐步绘制点即可，Lorenz的方程为：dx/dt = a(y-x), dy/dt = x(b-z)-y, dz/dt = xy - cz。设置初始点(x0,y0,z0)和参数a,b,c，然后利用x = x + dx/dt，y = y + dy/dt， z = z + dz/dt，进行得到一系列点，绘制即可。 <br>
      ![Lorenz曲线](https://github.com/lxcnju/fractals_py_p5/blob/master/pics/lorenz.png)
      * Peter De Jonge <br>
      利用分形火焰算法绘制Peter De Jonge的主要步骤为：(1)构建像素点矩阵，像素点数据结构colorPoint的属性包括：位置pos、颜色color、频率freq、透明度alpha；构建迭代过程所需要的数据结构iterStruc包括：初始位置(xn,yn)、颜色cn；(2)根据方程：xn1 = sin(a * yn) - cos(b * xn)，yn1 = sin(c * xn) - cos(d * yn)，cn1 = sin(e * xn) - cos(f * cn)，a~f为参数，xn,yn,cn为iterStruc里面对应的值，迭代一次得到xn1,yn1,cn1，然后根据j = floor(yn1 * scale + offset), i = floor(xn1 * scale + offset)将xn1,yn1转换为像素点位置(i,j)，然后更新(i,j)像素点数据结构colorPoint里面的频率和颜色，频率累加1，颜色color = (color + cn1)/2进行更新；最后更新iterStruc里面的xn,yn,cn = (cn + cn1)/2；(3)重复第2步maxIter次，比如200000次，则可以统计得到像素点的频次freq和颜色信息color；(4)统计得到所有像素点的最大频次maxFreq，然后计算透明度alpha = log(freq)/log(maxFreq)，更新颜色color = color * alpha ^ (1/gamma)，增加图像的对比度，显示出更多细节信息；(5)添加一些对称，左右对称、上下对称或中心对称，形成更完美的图形。<br>
      ![Peter De Jonge曲线-1](https://github.com/lxcnju/fractals_py_p5/blob/master/pics/attractor4.png)
      ![Peter De Jonge曲线-2](https://github.com/lxcnju/fractals_py_p5/blob/master/pics/attractor6.png)
  * Random Fractals
      * 介绍 <br>
      随机分形是利用一些随机游走的方法来构建的分析，比如自然界里面的山脉、河流和珊瑚树等等，都可以利用随机分形的技术进行计算机模拟。<br>
      * DLA <br>
      Diffusion Limited Aggregation是有限制地进行扩散凝聚，具体思想是初始化一些静态粒子和动态粒子，以及边界条件。刚开始模拟的时候，生成一些静态粒子，然后生成maxNum个动态粒子，动态粒子随机往各个方向游走，如果离静态粒子很近时则变为静态粒子停止运动，如果该粒子的位置超出了边界，则停止生长，待其余动态粒子全部变为静态粒子时算法停止；否则初始化一些新的动态粒子，保持maxNum个动态粒子在随机游走。<br>
      一般来说，随机游走生成图形耗时，需要大量的计算开销。<br>
      ![DLA随机游走](https://github.com/lxcnju/fractals_py_p5/blob/master/pics/tree4.png)
