import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Brick Breaker",
    page_icon="🧱",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background: #080b16;
    }

    h1 {
        text-align: center;
        color: white;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #8b93a7;
        margin-bottom: 20px;
    }

    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🧱 BRICK BREAKER")
st.markdown(
    '<div class="subtitle">← → 방향키 또는 A / D로 패들을 움직이세요!</div>',
    unsafe_allow_html=True
)

game_html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #080b16;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

.game-wrapper {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.hud {
    width: min(760px, 96vw);
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
    padding: 10px 5px;
    font-size: 15px;
    font-weight: bold;
}

.hud span {
    color: #67e8f9;
}

canvas {
    width: min(760px, 96vw);
    height: auto;
    aspect-ratio: 760 / 520;
    background: #0d1222;
    border-radius: 16px;
    box-shadow:
        0 0 25px rgba(103,232,249,.15),
        inset 0 0 30px rgba(0,0,0,.5);
    border: 1px solid #202a44;
}

.controls {
    display: flex;
    gap: 18px;
    margin-top: 15px;
}

.control-btn {
    width: 110px;
    height: 45px;
    border: none;
    border-radius: 12px;
    background: #151d33;
    color: white;
    font-size: 22px;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,.3);
}

.control-btn:active {
    transform: scale(.94);
    background: #24304f;
}

.menu {
    position: absolute;
    inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(8,11,22,.86);
    border-radius: 16px;
}

.menu-box {
    text-align: center;
    color: white;
}

.menu-title {
    font-size: 36px;
    font-weight: 900;
    margin-bottom: 10px;
}

.menu-text {
    color: #9ca7bd;
    margin-bottom: 22px;
}

.start-btn {
    padding: 13px 35px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(135deg, #67e8f9, #818cf8);
    color: #08101e;
    font-weight: 800;
    font-size: 17px;
    cursor: pointer;
}

.canvas-container {
    position: relative;
    width: min(760px, 96vw);
}
</style>
</head>

<body>

<div class="game-wrapper">

    <div class="hud">
        <div>SCORE <span id="score">0</span></div>
        <div>LEVEL <span id="level">1</span></div>
        <div>LIVES <span id="lives">3</span></div>
        <div>BEST <span id="best">0</span></div>
    </div>

    <div class="canvas-container">

        <canvas id="game" width="760" height="520"></canvas>

        <div class="menu" id="menu">
            <div class="menu-box">
                <div class="menu-title">🧱 BRICK BREAKER</div>
                <div class="menu-text">
                    Break every brick and clear all 3 levels!
                </div>
                <button class="start-btn" onclick="startGame()">
                    GAME START
                </button>
            </div>
        </div>

    </div>

    <div class="controls">
        <button class="control-btn" id="leftBtn">◀</button>
        <button class="control-btn" onclick="togglePause()">Ⅱ</button>
        <button class="control-btn" id="rightBtn">▶</button>
    </div>

</div>

<script>

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const W = canvas.width;
const H = canvas.height;

let score = 0;
let lives = 3;
let level = 1;
let best = Number(localStorage.getItem("brickBest") || 0);

document.getElementById("best").textContent = best;

let gameRunning = false;
let paused = false;

let keys = {
    left: false,
    right: false
};

let paddle = {
    width: 120,
    height: 13,
    x: W / 2 - 60,
    y: H - 35,
    speed: 8
};

let ball = {
    x: W / 2,
    y: H - 55,
    radius: 8,
    dx: 4,
    dy: -4
};

let bricks = [];

const brickColors = [
    "#67e8f9",
    "#818cf8",
    "#a78bfa",
    "#f472b6",
    "#fb7185",
    "#facc15"
];

function createBricks() {

    bricks = [];

    const rows = 4 + level;
    const cols = 9;

    const brickWidth = 68;
    const brickHeight = 22;

    const gap = 9;

    const totalWidth =
        cols * brickWidth +
        (cols - 1) * gap;

    const startX = (W - totalWidth) / 2;

    for (let r = 0; r < rows; r++) {

        for (let c = 0; c < cols; c++) {

            let hp = 1;

            if (level >= 2 && r === 0) {
                hp = 2;
            }

            if (level >= 3 && r === 0 && c % 3 === 0) {
                hp = 3;
            }

            bricks.push({
                x: startX + c * (brickWidth + gap),
                y: 55 + r * (brickHeight + gap),
                width: brickWidth,
                height: brickHeight,
                hp: hp,
                maxHp: hp,
                alive: true
            });
        }
    }
}

function resetBall() {

    ball.x = W / 2;
    ball.y = H - 55;

    const speed = 4 + (level - 1) * 0.7;

    ball.dx =
        (Math.random() > 0.5 ? 1 : -1) * speed;

    ball.dy = -speed;
}

function resetPaddle() {
    paddle.width = 120;
    paddle.x = W / 2 - paddle.width / 2;
}

function startGame() {

    score = 0;
    lives = 3;
    level = 1;

    gameRunning = true;
    paused = false;

    document.getElementById("menu").style.display = "none";

    createBricks();
    resetPaddle();
    resetBall();

    updateHUD();
}

function gameOver() {

    gameRunning = false;

    if (score > best) {
        best = score;
        localStorage.setItem("brickBest", best);
    }

    showMenu(
        "GAME OVER",
        "Your score: " + score
    );
}

function winGame() {

    gameRunning = false;

    if (score > best) {
        best = score;
        localStorage.setItem("brickBest", best);
    }

    showMenu(
        "🎉 YOU WIN!",
        "Final score: " + score
    );
}

function showMenu(title, text) {

    const menu = document.getElementById("menu");

    menu.innerHTML = `
        <div class="menu-box">
            <div class="menu-title">${title}</div>
            <div class="menu-text">${text}</div>
            <button class="start-btn" onclick="startGame()">
                PLAY AGAIN
            </button>
        </div>
    `;

    menu.style.display = "flex";
}

function togglePause() {

    if (!gameRunning) return;

    paused = !paused;
}

function updateHUD() {

    document.getElementById("score").textContent = score;
    document.getElementById("level").textContent = level;
    document.getElementById("lives").textContent = lives;
    document.getElementById("best").textContent = best;
}

function update() {

    if (!gameRunning || paused) return;

    // paddle movement

    if (keys.left) {
        paddle.x -= paddle.speed;
    }

    if (keys.right) {
        paddle.x += paddle.speed;
    }

    paddle.x = Math.max(
        0,
        Math.min(W - paddle.width, paddle.x)
    );

    // ball movement

    ball.x += ball.dx;
    ball.y += ball.dy;

    // left/right walls

    if (ball.x - ball.radius <= 0) {
        ball.x = ball.radius;
        ball.dx *= -1;
    }

    if (ball.x + ball.radius >= W) {
        ball.x = W - ball.radius;
        ball.dx *= -1;
    }

    // top wall

    if (ball.y - ball.radius <= 0) {
        ball.y = ball.radius;
        ball.dy *= -1;
    }

    // paddle collision

    if (
        ball.y + ball.radius >= paddle.y &&
        ball.y - ball.radius <= paddle.y + paddle.height &&
        ball.x >= paddle.x &&
        ball.x <= paddle.x + paddle.width &&
        ball.dy > 0
    ) {

        const hitPosition =
            (ball.x - paddle.x) / paddle.width;

        const angle =
            (hitPosition - 0.5) * Math.PI * 0.75;

        const speed =
            Math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy);

        ball.dx = Math.sin(angle) * speed;
        ball.dy = -Math.abs(Math.cos(angle) * speed);

        ball.y = paddle.y - ball.radius;
    }

    // brick collision

    for (let brick of bricks) {

        if (!brick.alive) continue;

        if (
            ball.x + ball.radius > brick.x &&
            ball.x - ball.radius < brick.x + brick.width &&
            ball.y + ball.radius > brick.y &&
            ball.y - ball.radius < brick.y + brick.height
        ) {

            brick.hp--;

            if (brick.hp <= 0) {

                brick.alive = false;

                score += brick.maxHp * 10;

                // small chance of power-up
                if (Math.random() < 0.10) {
                    // reserved for future power-up system
                }

            } else {

                score += 5;
            }

            ball.dy *= -1;

            break;
        }
    }

    // check level clear

    const remaining =
        bricks.filter(b => b.alive).length;

    if (remaining === 0) {

        if (level >= 3) {

            score += 100;
            updateHUD();
            winGame();

            return;
        }

        score += 100;
        level++;

        createBricks();
        resetBall();

        updateHUD();
    }

    // ball falls

    if (ball.y - ball.radius > H) {

        lives--;

        if (lives <= 0) {

            updateHUD();
            gameOver();

            return;

        } else {

            resetBall();
            resetPaddle();
        }
    }

    updateHUD();
}

function drawBackground() {

    ctx.fillStyle = "#0d1222";
    ctx.fillRect(0, 0, W, H);

    // subtle grid

    ctx.strokeStyle = "rgba(255,255,255,0.025)";
    ctx.lineWidth = 1;

    for (let x = 0; x < W; x += 40) {

        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, H);
        ctx.stroke();
    }

    for (let y = 0; y < H; y += 40) {

        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(W, y);
        ctx.stroke();
    }
}

function drawPaddle() {

    const gradient =
        ctx.createLinearGradient(
            paddle.x,
            paddle.y,
            paddle.x + paddle.width,
            paddle.y
        );

    gradient.addColorStop(0, "#67e8f9");
    gradient.addColorStop(1, "#818cf8");

    ctx.fillStyle = gradient;

    roundRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height,
        7
    );

    ctx.shadowBlur = 18;
    ctx.shadowColor = "#67e8f9";
    ctx.fill();

    ctx.shadowBlur = 0;
}

function drawBall() {

    const gradient =
        ctx.createRadialGradient(
            ball.x - 3,
            ball.y - 3,
            1,
            ball.x,
            ball.y,
            ball.radius
        );

    gradient.addColorStop(0, "#ffffff");
    gradient.addColorStop(0.4, "#67e8f9");
    gradient.addColorStop(1, "#818cf8");

    ctx.fillStyle = gradient;

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fill();

    ctx.shadowBlur = 20;
    ctx.shadowColor = "#67e8f9";

    ctx.fill();

    ctx.shadowBlur = 0;
}

function drawBricks() {

    bricks.forEach((brick, index) => {

        if (!brick.alive) return;

        let color =
            brickColors[index % brickColors.length];

        if (brick.hp === 2) {
            color = "#facc15";
        }

        if (brick.hp === 3) {
            color = "#fb7185";
        }

        ctx.fillStyle = color;

        roundRect(
            brick.x,
            brick.y,
            brick.width,
            brick.height,
            6
        );

        ctx.fill();

        // highlight

        ctx.fillStyle = "rgba(255,255,255,.22)";

        roundRect(
            brick.x + 3,
            brick.y + 3,
            brick.width - 6,
            4,
            3
        );

        ctx.fill();
    });
}

function roundRect(x, y, w, h, r) {

    ctx.beginPath();

    ctx.moveTo(x + r, y);

    ctx.arcTo(
        x + w,
        y,
        x + w,
        y + h,
        r
    );

    ctx.arcTo(
        x + w,
        y + h,
        x,
        y + h,
        r
    );

    ctx.arcTo(
        x,
        y + h,
        x,
        y,
        r
    );

    ctx.arcTo(
        x,
        y,
        x + w,
        y,
        r
    );

    ctx.closePath();
}

function drawPause() {

    if (!paused) return;

    ctx.fillStyle = "rgba(0,0,0,.55)";
    ctx.fillRect(0, 0, W, H);

    ctx.fillStyle = "white";
    ctx.font = "bold 42px Arial";
    ctx.textAlign = "center";

    ctx.fillText(
        "PAUSED",
        W / 2,
        H / 2
    );
}

function draw() {

    drawBackground();
    drawBricks();
    drawPaddle();
    drawBall();
    drawPause();
}

function loop() {

    update();
    draw();

    requestAnimationFrame(loop);
}

// keyboard controls

document.addEventListener("keydown", e => {

    if (
        e.key === "ArrowLeft" ||
        e.key.toLowerCase() === "a"
    ) {
        keys.left = true;
        e.preventDefault();
    }

    if (
        e.key === "ArrowRight" ||
        e.key.toLowerCase() === "d"
    ) {
        keys.right = true;
        e.preventDefault();
    }

    if (e.key === " ") {
        togglePause();
        e.preventDefault();
    }
});

document.addEventListener("keyup", e => {

    if (
        e.key === "ArrowLeft" ||
        e.key.toLowerCase() === "a"
    ) {
        keys.left = false;
    }

    if (
        e.key === "ArrowRight" ||
        e.key.toLowerCase() === "d"
    ) {
        keys.right = false;
    }
});

// mobile buttons

function holdButton(button, direction) {

    button.addEventListener("mousedown", () => {
        keys[direction] = true;
    });

    button.addEventListener("mouseup", () => {
        keys[direction] = false;
    });

    button.addEventListener("mouseleave", () => {
        keys[direction] = false;
    });

    button.addEventListener("touchstart", e => {
        e.preventDefault();
        keys[direction] = true;
    });

    button.addEventListener("touchend", e => {
        e.preventDefault();
        keys[direction] = false;
    });
}

holdButton(
    document.getElementById("leftBtn"),
    "left"
);

holdButton(
    document.getElementById("rightBtn"),
    "right"
);

createBricks();
draw();
loop();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=650,
    scrolling=False
)
