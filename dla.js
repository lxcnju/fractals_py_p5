// diffusion limited aggregation
// 基本思想是初始化一群静态粒子和一群运动的粒子
// 运动的粒子随机运动，如果碰到静态粒子，则也变为静态粒子，构建新的动态粒子加入，继续运动
// 当有一个静态粒子触及到了停止边界时，停止加入新的动态粒子，等待剩余所有的动态粒子停止运动则算法停止

var staticParticles = [];       // 静态粒子
var moveParticles = [];         // 动态粒子
var maxNum = 500;               // 粒子数组里面最多的粒子数目
var speedIters = 20;            // 每隔20词显示一次
var stopGrow = false;           // 是否停止生长

function setup(){
	createCanvas(200, 200);
	var p = new particle(width, height, false);    // 静止的粒子
	p.initialize();
	staticParticles.push(p);
	
	for(var i = 0; i < maxNum; i++){
		p = new particle(width, height, true);     // 运动的粒子
		p.initialize();
		moveParticles.push(p);
	}
}

function draw(){
	background(255);
	// 显示
	for(var i = moveParticles.length - 1; i >= 0 ; i--){
		moveParticles[i].moveAndShow();
	}
	for(var j = 0; j < staticParticles.length; j++){
		staticParticles[j].moveAndShow();
		// 有一个静态粒子到达了边界，则停止
		if(staticParticles[j].outBorder()){
			stopGrow = true;
		}
	}
	// 迭代更新
	for(var k = 0; k < speedIters; k++){
		for(var i = moveParticles.length - 1; i > 0 ; i--){
			var mp = moveParticles[i];
			var toBeStatic = false;
			var startIndex = max(0, staticParticles.length - 100);
			if(stopGrow == true){
				startIndex = 0;
			}
			for(var j = startIndex; j < staticParticles.length; j++){
				if(mp.checkDistance(staticParticles[j]) == true){
					toBeStatic = true;
					break;
				}
			}
			if(toBeStatic == true){
				mp.toStatic();
				staticParticles.push(mp);
				moveParticles.splice(i, 1);
			}
		}
	}
	while(moveParticles.length < maxNum && stopGrow == false){
		p = new particle(width, height, true);
		p.initialize();
		moveParticles.push(p);
	}
}


// moving表示运动或静止;false是静止，true是运动
function particle(width, height, moving){
	this.width = width;                              // 图像大小
	this.height = height;
	this.moving = moving;                            // 是否运动
	this.pos = createVector(height/2, width/2);      // 粒子位置
	this.vel = p5.Vector.random2D();                 // 粒子速度
	this.stepSize = 1.0;                             // 粒子速度的模长
	this.radius = 1.5;                               // 粒子半径
	this.distThreshold = 1.2 * this.radius;            // 粒子距离中心距离界限
	// 初始化，如果静止，则什么都不做，默认在图像中心点；否则随机在四周初始化粒子
	this.initialize = function(){
		if(this.moving == false){
			return;
		}
		var rn = random(0, 4);
		// 上-->右-->下-->左
		if(rn < 1.0){
			this.pos.x = random(0, this.width);
			this.pos.y = 0.0;
		}else if(rn < 2.0){
			this.pos.x = this.width;
			this.pos.y = random(0, this.height);
		}else if(rn < 3.0){
			this.pos.x = random(0, this.width);
			this.pos.y = this.height;
		}else{
			this.pos.x = 0.0;
			this.pos.y = random(0, this.height);
		}
	}
	// 按照随机生成的速度进行运动；如果是静态粒子，则不移动，直接显示，否则先运动再显示
	this.moveAndShow = function(){
		noStroke();
		if(this.moving == true){
			fill(random(200, 255), random(50, 100), 100);
			this.vel = p5.Vector.random2D();              // 随机方向
			this.vel.mult(this.stepSize);
			this.pos.add(this.vel);
			this.pos.x = constrain(this.pos.x, 0, this.width);    // 限制在图像内部
			this.pos.y = constrain(this.pos.y, 0, this.height);
		}else{
			fill(0);
		}
		ellipse(this.pos.x, this.pos.y, this.radius, this.radius);
	}
	// 检查和静态粒子的距离
	this.checkDistance = function(stPart){
		var dis = this.pos.dist(stPart.pos);
		if(dis <= this.distThreshold){
			if(random(1) < 0.1){
				return true;
			}
		}
		return false;
	}
	// 改变状态
	this.toStatic = function(){
		this.moving = false;
	}
	// 是否超出边界
	this.outBorder = function(){
		if(this.pos.x < 0 || this.pos.x > this.width || this.pos.y < 0 || this.pos.y > this.height){
			return true;
		}
		return false;
	}
}