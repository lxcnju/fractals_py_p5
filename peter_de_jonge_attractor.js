// Attractor分形绘制 + Flame算法 + Density Esitimation + Tone mapping进行图像渲染

var attrac;
var offsetWidth;          // tanslate的偏移量
var offsetHeight;

function setup() {
	createCanvas(300, 300);
	offsetHeight = height / 2;             // 移动到中心
	offsetWidth = width / 2;
	
	attrac = new myAttractor(width, height);
	attrac.makePoints();
	attrac.toSymmetric();
}

function draw() {
	background(255);
	translate(offsetWidth, offsetHeight);  //平移至中心
	
	attrac.display();
}

function myAttractor(w, h){
	this.a = random(-3, 3);                    // 迭代函数的参数
	this.b = random(-3, 3);
	this.c = random(-3, 3);
	this.d = random(-3, 3);
	this.e = random(-3, 3);
	this.f = random(-3, 3);
	
	console.log(this.a, this.b, this.c, this.d, this.e, this.f);
	
	this.maxIter = 2000000;                     // 最多迭代次数
	
	this.scale = floor(min(w, h) * 0.4);       // 放大的倍数
	
	this.width = w;                   // 图像大小
	this.height = h;
	
	this.freqMax = 0;                 // 最高像素点频率
	
	this.gamma = 2.0;                 // gamma渲染
	
	this.itst = new iterStruc();      // 迭代过程的结果保存，xn yn color等等
	this.points = [];                 // 像素点
	
	this.redParam1 = 0.0;             // 颜色前面的系数
	this.greenParam1 = 0.0;
	this.blueParam1 = 0.0;
	this.redParam2 = 0.0;
	this.greenParam2 = 0.0;
	this.blueParam2 = 0.0;
	
	// 构造像素点
	this.makePoints = function(){
		// 初始化
		for(var j = 0; j < this.height; j++){
			var rowPoints = [];
			for(var i = 0; i < this.width; i++){
				rowPoints.push(new colorPoint(j, i));
			}
			this.points.push(rowPoints);
		}
		// 迭代
		for(var k = 0; k < this.maxIter; k++){
			this.iterateFunction();
		}
		// 求最高频率,然后利用频率进行对数归一化得到alpha
		for(var j = 0; j < this.height; j++){
			for(var i = 0; i < this.width; i++){
				this.freqMax = max(this.freqMax, this.points[j][i].freq);
			}
		}
		var toDivide = log(this.freqMax);
		if(toDivide != 0.0){
			for(var j = 0; j < this.height; j++){
				for(var i = 0; i < this.width; i++){
					if(this.points[j][i].freq != 0.0){
						this.points[j][i].alpha = log(this.points[j][i].freq) / toDivide;
					}
				}
			}
		}
		// gamma渲染,增强图像
		for(var j = 0; j < this.height; j++){
			for(var i = 0; i < this.width; i++){
				this.points[j][i].color = this.points[j][i].color * pow(this.points[j][i].alpha, 1 / this.gamma);
				if(j % 50 == 0 && i % 50 == 0){
					console.log(this.points[j][i].color);
				}
			}
		}
	}
	// 将像素点进行对称
	this.toSymmetric = function(){
		var rn = floor(random(0, 3));
		console.log(rn);
		if(rn == 0){
			// 上下对称
			for(var j = floor(this.height)/2; j < this.height; j++){
				for(var i = 0; i < this.width; i++){
					var p1 = this.points[j][i];
					var p2 = this.points[this.height - 1 - j][i];
					var freqSum = floor(p1.freq + p2.freq);
					var colorMean = (p1.color + p2.color)/2;
					this.points[j][i].freq = freqSum;
					this.points[j][i].color = colorMean;
					this.points[this.height - j - 1][i].freq = freqSum;
					this.points[this.height - j - 1][i].color = colorMean;
				}
			}
		}else if(rn == 1){
			// 左右
			for(var j = 0; j < this.height; j++){
				for(var i = floor(this.width/2); i < this.width; i++){
					var p1 = this.points[j][i];
					var p2 = this.points[j][this.width - i];
					var freqSum = floor(p1.freq + p2.freq);
					var colorMean = (p1.color + p2.color)/2;
					this.points[j][i].freq = freqSum;
					this.points[j][i].color = colorMean;
					this.points[j][this.width - i - 1].freq = freqSum;
					this.points[j][this.width - i - 1].color = colorMean;
				}
			}
		}else if(rn == 2){
			// 中心对称
			for(var j = 0; j < this.height; j++){
				for(var i = floor(this.width/2); i < this.width; i++){
					var p1 = this.points[j][i];
					var p2 = this.points[this.height - 1 - j][this.width - 1 - i];
					var freqSum = floor(p1.freq + p2.freq);
					var colorMean = (p1.color + p2.color)/2;
					this.points[j][i].freq = freqSum;
					this.points[j][i].color = colorMean;
					this.points[this.height - 1 - j][this.width - 1 - i].freq = freqSum;
					this.points[this.height - 1 - j][this.width - 1 - i].color = colorMean;
				}
			}
		}
	}
	// 逐个像素点显示
	this.display = function(){
		this.randomSetColorParams();
		beginShape(POINTS);
		for(var j = 0; j < this.height; j++){
			for(var i = 0; i < this.width; i++){
				var r = this.toRed(this.points[j][i].color);
				var g = this.toGreen(this.points[j][i].color);
				var b = this.toBlue(this.points[j][i].color);
				stroke(r, g, b);
				for(var k = 0; k < this.points[j][i].freq; k++){
					point(j - offsetHeight, i - offsetWidth);
				}
			}
		}
		endShape();
	}
	// 对点进行迭代，包括坐标和颜色
	this.iterateFunction = function(){
		var xn1 = sin(this.a * this.itst.yn) - cos(this.b * this.itst.xn);
		var yn1 = sin(this.c * this.itst.xn) - cos(this.d * this.itst.yn);
		var color = sin(this.e * this.itst.xn) - cos(this.f * this.itst.color);
		
		var j = this.toRowIndex(yn1);
		var i = this.toColIndex(xn1);
		
		if(j >= 0 && i >= 0 && j < this.height && i < this.width){
			this.points[j][i].freq += 1;
			this.points[j][i].color = (this.points[j][i].color + color) / 2;
		}
		
		this.itst.xn = xn1;
		this.itst.yn = yn1;
		this.itst.color = (color + this.itst.color) / 2;
	}
	// 将值转换为行index
	this.toRowIndex = function(yn){
		return floor(yn * this.scale + offsetHeight);
	}
	this.toColIndex = function(xn){
		return floor(xn * this.scale + offsetWidth);
	}
	// 生成r颜色
	this.toRed = function(color){
		var c = abs(color)/1.732;
		var r = floor(255 * (this.redParam1 + this.redParam1 * c));
		return r;
	}
	this.toGreen = function(color){
		var c = abs(color)/1.732;
		var g = floor(255 * (this.greenParam1 + this.greenParam2 * c));
		return g;
	}
	this.toBlue = function(color){
		var c = abs(color)/1.732;
		var b = floor(255 * (this.blueParam1 + this.blueParam2 * c));
		return b;
	}
	this.randomSetColorParams = function(){
		this.redParam1 = random(0, 1);             // 颜色前面的系数
		this.greenParam1 = random(0, 1);
		this.blueParam1 = random(0, 1);
		this.redParam2 = random(-this.redParam1, 1 - this.redParam1);
		this.greenParam2 = random(-this.greenParam1, 1 - this.greenParam1);
		this.blueParam2 = random(-this.blueParam1, 1 - this.blueParam1);
	}
}

function iterStruc(){
	this.xn = 0.0;
	this.yn = 0.5;
	
	this.color = 0;
}

function colorPoint(j, i){
	this.j = j;           // 在图像上的坐标
	this.i = i;
	
	this.color = 0;      // 颜色
	this.freq = 0;       // 计数
	this.alpha = 1.0;      // 颜色透明度
}