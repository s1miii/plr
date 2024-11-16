const canvas = document.getElementById('heartsCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const heartsArray = [];
const colors = ['#ff6b6b', '#ff8e72', '#ffb6b9', '#ff6f91', '#ff9671'];

class Heart {
  constructor() {
    this.size = Math.random() * 20 + 10;
    this.x = Math.random() * canvas.width;
    this.y = canvas.height + this.size;
    this.speed = Math.random() * 1 + 0.5;
    this.color = colors[Math.floor(Math.random() * colors.length)];
    this.opacity = Math.random() * 0.5 + 0.5;
  }

  draw() {
    ctx.globalAlpha = this.opacity;
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.moveTo(this.x, this.y);
    ctx.bezierCurveTo(this.x + this.size / 2, this.y - this.size / 2, this.x + this.size, this.y + this.size / 3, this.x, this.y + this.size);
    ctx.bezierCurveTo(this.x - this.size, this.y + this.size / 3, this.x - this.size / 2, this.y - this.size / 2, this.x, this.y);
    ctx.closePath();
    ctx.fill();
  }

  update() {
    this.y -= this.speed;
    if (this.y < -this.size) {
      this.y = canvas.height + this.size;
      this.x = Math.random() * canvas.width;
      this.size = Math.random() * 20 + 10;
      this.speed = Math.random() * 1 + 0.5;
      this.color = colors[Math.floor(Math.random() * colors.length)];
      this.opacity = Math.random() * 0.5 + 0.5;
    }
    this.draw();
  }
}

function init() {
  for (let i = 0; i < 100; i++) {
    heartsArray.push(new Heart());
  }
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  heartsArray.forEach(heart => heart.update());
  requestAnimationFrame(animate);
}

init();
animate();

window.addEventListener('resize', () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
});
