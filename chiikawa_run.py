import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

# =========================================================
# Streamlit 설정
# =========================================================

st.set_page_config(
    page_title="Chiikawa Run!",
    page_icon="🌸",
    layout="centered"
)

# =========================================================
# 이미지 불러오기
# =========================================================

BASE_DIR = Path(__file__).parent
ASSETS = BASE_DIR / "assets"


def image_to_base64(filename):
    path = ASSETS / filename

    if not path.exists():
        return ""

    ext = path.suffix.lower()

    if ext == ".png":
        mime = "image/png"
    elif ext in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    else:
        mime = "image/png"

    data = base64.b64encode(path.read_bytes()).decode("utf-8")

    return f"data:{mime};base64,{data}"


CHARACTER1 = image_to_base64("character1.png")
CHARACTER2 = image_to_base64("character2.png")
CHARACTER3 = image_to_base64("character3.png")
BACKGROUND = image_to_base64("background.jpg")


# =========================================================
# Streamlit 배경
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(
            180deg,
            #dff6ff,
            #fff0f5
        );
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 10px;
        padding-bottom: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 게임 HTML
# =========================================================

game = """
<!DOCTYPE html>
<html lang="ko">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0,
             maximum-scale=1.0,
             user-scalable=no"
>

<style>

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0;
    padding: 0;
    width: 100%;
    background: transparent;
    overflow: hidden;
    font-family:
        Arial,
        "Apple SD Gothic Neo",
        sans-serif;
}

.game-container {
    width: 100%;
    display: flex;
    justify-content: center;
}

.game {
    position: relative;
    width: min(920px, 100vw);
}

canvas {
    width: 100%;
    height: auto;
    display: block;

    border-radius: 24px;

    box-shadow:
        0 12px 35px
        rgba(80, 50, 70, 0.25);
}


/* =====================================================
   HUD
===================================================== */

.hud {
    position: absolute;

    top: 12px;
    left: 14px;
    right: 14px;

    display: flex;
    justify-content: space-between;

    z-index: 5;

    pointer-events: none;
}

.hud-box {
    background: rgba(255, 255, 255, 0.90);

    padding: 7px 12px;

    border-radius: 14px;

    color: #604850;

    font-weight: 900;

    font-size: 15px;

    box-shadow:
        0 4px 12px
        rgba(0, 0, 0, 0.12);
}


/* =====================================================
   시작 / 게임오버 메뉴
===================================================== */

.menu {
    position: absolute;

    inset: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    background: rgba(255, 255, 255, 0.28);

    border-radius: 24px;

    z-index: 10;

    overflow: hidden;

    padding: 12px;
}

.card {
    width: min(430px, 90%);

    max-height: 94%;

    overflow-y: auto;

    padding: 20px 18px;

    text-align: center;

    background: rgba(255, 255, 255, 0.97);

    border-radius: 24px;

    box-shadow:
        0 15px 40px
        rgba(70, 50, 70, 0.25);
}

.title {
    font-size: clamp(24px, 6vw, 34px);

    font-weight: 900;

    color: #5d3f47;

    margin-bottom: 10px;
}

.description {
    color: #77666d;

    line-height: 1.45;

    margin-bottom: 16px;

    font-size: clamp(14px, 3.5vw, 17px);
}

.start-button {
    border: none;

    padding: 12px 26px;

    border-radius: 17px;

    background:
        linear-gradient(
            135deg,
            #ff93b7,
            #ff6797
        );

    color: white;

    font-size: 16px;

    font-weight: 900;

    cursor: pointer;

    box-shadow:
        0 5px 0 #d84e79;
}

.start-button:active {
    transform: translateY(4px);
    box-shadow: none;
}


/* =====================================================
   모바일 조작
===================================================== */

.controls {
    position: absolute;

    bottom: 12px;

    left: 50%;

    transform: translateX(-50%);

    display: flex;

    gap: 7px;

    z-index: 8;
}

.control {
    width: 48px;
    height: 44px;

    border: none;

    border-radius: 14px;

    background: rgba(255, 255, 255, 0.90);

    font-size: 19px;

    cursor: pointer;

    box-shadow:
        0 4px 10px
        rgba(0, 0, 0, 0.15);

    -webkit-tap-highlight-color: transparent;
}


/* =====================================================
   모바일 화면
===================================================== */

@media (max-width: 600px) {

    .game {
        width: 100%;
    }

    canvas {
        border-radius: 18px;
    }

    .menu {
        padding: 8px;
        border-radius: 18px;
    }

    .card {
        width: 91%;
        max-height: 90%;
        padding: 17px 14px;
        border-radius: 21px;
    }

    .title {
        font-size: 24px;
        margin-bottom: 8px;
    }

    .description {
        font-size: 13px;
        line-height: 1.35;
        margin-bottom: 11px;
    }

    .start-button {
        padding: 10px 22px;
        font-size: 15px;
    }

    .hud {
        top: 8px;
        left: 9px;
        right: 9px;
    }

    .hud-box {
        padding: 6px 9px;
        font-size: 13px;
    }

    .controls {
        bottom: 9px;
        gap: 6px;
    }

    .control {
        width: 44px;
        height: 40px;
        font-size: 18px;
    }
}

</style>

</head>


<body>

<div class="game-container">

<div class="game">

<canvas
    id="gameCanvas"
    width="920"
    height="650">
</canvas>


<!-- HUD -->

<div class="hud">

    <div class="hud-box">
        ⭐ <span id="score">0</span>
    </div>

    <div class="hud-box">
        🏆 <span id="best">0</span>
    </div>

    <div class="hud-box">
        🎭 <span id="form">기본 치이카와</span>
    </div>

</div>


<!-- 시작 / 게임오버 화면 -->

<div
    class="menu"
    id="menu"
>

    <div class="card">

        <div class="title">
            🌸 CHIIKAWA RUN! 🌸
        </div>

        <div class="description">

            치이카와 친구들과 함께 달려보세요! 🏃💨

            <br><br>

            ◀ ▶ 레인 이동<br>

            ⬆ / SPACE 점프<br>

            ⬇ 슬라이드

            <br><br>

            🎁 랜덤박스를 먹으면<br>

            좋은 아이템과 나쁜 아이템이<br>

            랜덤으로 등장합니다!

            <br><br>

            🎭 점수가 올라가면<br>

            치이카와가 변신합니다!

        </div>

        <button
            class="start-button"
            onclick="startGame()"
        >
            START RUN! 🏃
        </button>

    </div>

</div>


<!-- 모바일 조작 버튼 -->

<div class="controls">

    <button
        class="control"
        onclick="moveLeft()"
    >
        ◀
    </button>

    <button
        class="control"
        onclick="jump()"
    >
        ⬆
    </button>

    <button
        class="control"
        onclick="moveRight()"
    >
        ▶
    </button>

    <button
        class="control"
        onclick="slide()"
    >
        ⬇
    </button>

</div>

</div>

</div>


<script>

// =====================================================
// 이미지
// =====================================================

const character1 = new Image();
character1.src = "__CHARACTER1__";

const character2 = new Image();
character2.src = "__CHARACTER2__";

const character3 = new Image();
character3.src = "__CHARACTER3__";

const background = new Image();
background.src = "__BACKGROUND__";


// =====================================================
// 캔버스
// =====================================================

const canvas =
    document.getElementById("gameCanvas");

const ctx =
    canvas.getContext("2d");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;


// =====================================================
// 게임 상태
// =====================================================

let gameRunning = false;

let score = 0;

let bestScore =
    Number(
        localStorage.getItem("chiikawa_best") || 0
    );

let gameSpeed = 7;

let distance = 0;

let spawnTimer = 30;

let objects = [];

let particles = [];


// =====================================================
// 레인
// =====================================================

const lanes = [
    300,
    460,
    620
];


// =====================================================
// 플레이어
// =====================================================

let player = {
    lane: 1,
    x: 460,
    targetX: 460,

    y: 515,

    velocityY: 0,

    jumping: false,

    sliding: false,

    slideTimer: 0,

    giant: false,

    giantTimer: 0,

    shield: false,

    shieldTimer: 0,

    transformation: 0,

    turning: false,

    turnTimer: 0,

    rotation: 0
};


// =====================================================
// 시작
// =====================================================

function startGame() {

    score = 0;

    distance = 0;

    gameSpeed = 7;

    spawnTimer = 30;

    objects = [];

    particles = [];

    player = {
        lane: 1,
        x: 460,
        targetX: 460,

        y: 515,

        velocityY: 0,

        jumping: false,

        sliding: false,

        slideTimer: 0,

        giant: false,

        giantTimer: 0,

        shield: false,

        shieldTimer: 0,

        transformation: 0,

        turning: false,

        turnTimer: 0,

        rotation: 0
    };

    gameRunning = true;

    document
        .getElementById("menu")
        .style.display = "none";
}


// =====================================================
// 이동
// =====================================================

function moveLeft() {

    if (!gameRunning)
        return;

    if (player.lane > 0) {

        player.lane--;

        player.targetX =
            lanes[player.lane];
    }
}


function moveRight() {

    if (!gameRunning)
        return;

    if (player.lane < 2) {

        player.lane++;

        player.targetX =
            lanes[player.lane];
    }
}


// =====================================================
// 점프
// =====================================================

function jump() {

    if (!gameRunning)
        return;

    if (!player.jumping) {

        player.jumping = true;

        player.velocityY = -18;

        player.rotation = 0;
    }
}


// =====================================================
// 슬라이드
// =====================================================

function slide() {

    if (!gameRunning)
        return;

    if (!player.jumping) {

        player.sliding = true;

        player.slideTimer = 40;
    }
}


// =====================================================
// 키보드
// =====================================================

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "ArrowLeft") {

            moveLeft();
            event.preventDefault();
        }

        if (event.key === "ArrowRight") {

            moveRight();
            event.preventDefault();
        }

        if (
            event.key === "ArrowUp" ||
            event.code === "Space"
        ) {

            jump();
            event.preventDefault();
        }

        if (event.key === "ArrowDown") {

            slide();
            event.preventDefault();
        }
    }
);


// =====================================================
// 오브젝트 생성
// =====================================================

function spawnObject() {

    const lane =
        Math.floor(Math.random() * 3);

    const random =
        Math.random();

    let type;

    if (random < 0.45) {

        type = "obstacle";

    } else if (random < 0.70) {

        type = "box";

    } else {

        type = "item";
    }

    let item = null;

    if (type === "item") {

        const r = Math.random();

        if (r < 0.18)
            item = "giant";

        else if (r < 0.36)
            item = "score";

        else if (r < 0.52)
            item = "shield";

        else if (r < 0.68)
            item = "slow";

        else if (r < 0.84)
            item = "speed";

        else
            item = "bad";
    }

    objects.push({

        lane: lane,

        x: lanes[lane],

        y: -80,

        type: type,

        item: item
    });
}


// =====================================================
// 아이템 효과
// =====================================================

function activateItem(item) {

    if (item === "giant") {

        player.giant = true;

        player.giantTimer = 420;
    }

    if (item === "score") {

        score += 500;
    }

    if (item === "shield") {

        player.shield = true;

        player.shieldTimer = 360;
    }

    if (item === "slow") {

        gameSpeed =
            Math.max(
                4,
                gameSpeed - 2
            );
    }

    if (item === "speed") {

        score += 250;

        gameSpeed =
            Math.min(
                16,
                gameSpeed + 1
            );
    }

    if (item === "bad") {

        score =
            Math.max(
                0,
                score - 350
            );

        gameSpeed =
            Math.min(
                16,
                gameSpeed + 2
            );
    }
}


// =====================================================
// 랜덤박스
// =====================================================

function openBox(obj) {

    const r = Math.random();

    let item;

    if (r < 0.20)
        item = "giant";

    else if (r < 0.40)
        item = "score";

    else if (r < 0.58)
        item = "shield";

    else if (r < 0.72)
        item = "slow";

    else if (r < 0.86)
        item = "speed";

    else
        item = "bad";

    activateItem(item);

    createParticles(
        obj.x,
        obj.y,
        "#ffd447",
        25
    );
}


// =====================================================
// 충돌
// =====================================================

function collision(a, b) {

    return (
        Math.abs(a.x - b.x) < 55 &&
        Math.abs(a.y - b.y) < 70
    );
}


// =====================================================
// 변신
// =====================================================

function checkTransformation() {

    let newForm = 0;

    if (score >= 5000) {

        newForm = 2;

    } else if (score >= 2500) {

        newForm = 1;
    }

    if (
        newForm >
        player.transformation
    ) {

        player.transformation =
            newForm;

        player.turning = true;

        player.turnTimer = 120;
    }

    let formText =
        "기본 치이카와";

    if (
        player.transformation === 1
    ) {

        formText =
            "✨ 변신 치이카와";
    }

    if (
        player.transformation === 2
    ) {

        formText =
            "👑 최종 치이카와";
    }

    document
        .getElementById("form")
        .textContent =
        formText;
}


// =====================================================
// 게임 업데이트
// =====================================================

function update() {

    if (!gameRunning)
        return;

    distance += gameSpeed;

    score += 0.28;

    gameSpeed =
        Math.min(
            16,
            7 + distance / 6500
        );

    checkTransformation();


    // 레인 이동

    player.x +=
        (
            player.targetX -
            player.x
        ) * 0.2;


    // 점프

    if (player.jumping) {

        player.velocityY += 1;

        player.y +=
            player.velocityY;

        if (player.y >= 515) {

            player.y = 515;

            player.velocityY = 0;

            player.jumping = false;
        }
    }


    // 슬라이드

    if (player.sliding) {

        player.slideTimer--;

        if (player.slideTimer <= 0) {

            player.sliding = false;
        }
    }


    // 거대화

    if (player.giant) {

        player.giantTimer--;

        if (player.giantTimer <= 0) {

            player.giant = false;
        }
    }


    // 보호막

    if (player.shield) {

        player.shieldTimer--;

        if (player.shieldTimer <= 0) {

            player.shield = false;
        }
    }


    // 변신 애니메이션

    if (player.turning) {

        player.turnTimer--;

        if (player.turnTimer <= 0) {

            player.turning = false;
        }
    }


    // 오브젝트 생성

    spawnTimer--;

    if (spawnTimer <= 0) {

        spawnObject();

        spawnTimer =
            Math.max(
                28,
                75 - gameSpeed * 2
            );
    }


    // 오브젝트 이동

    objects.forEach(
        function(obj) {

            obj.y += gameSpeed;
        }
    );


    objects =
        objects.filter(
            function(obj) {

                return obj.y <
                    HEIGHT + 100;
            }
        );


    // 충돌 처리

    for (
        let i = objects.length - 1;
        i >= 0;
        i--
    ) {

        const obj = objects[i];

        if (
            !collision(
                player,
                obj
            )
        ) {
            continue;
        }


        // 랜덤박스

        if (
            obj.type === "box"
        ) {

            openBox(obj);

            objects.splice(i, 1);

            continue;
        }


        // 아이템

        if (
            obj.type === "item"
        ) {

            activateItem(obj.item);

            objects.splice(i, 1);

            continue;
        }


        // 장애물

        if (
            obj.type === "obstacle"
        ) {

            // 점프 중이면 통과

            if (player.jumping)
                continue;


            // 거대화

            if (player.giant) {

                score += 200;

                createParticles(
                    obj.x,
                    obj.y,
                    "#ff82a8",
                    20
                );

                objects.splice(i, 1);

                continue;
            }


            // 보호막

            if (player.shield) {

                objects.splice(i, 1);

                continue;
            }


            gameOver();

            return;
        }
    }

    updateParticles();
}


// =====================================================
// 게임오버
// =====================================================

function gameOver() {

    gameRunning = false;

    if (score > bestScore) {

        bestScore =
            Math.floor(score);

        localStorage.setItem(
            "chiikawa_best",
            bestScore
        );
    }

    document
        .getElementById("menu")
        .innerHTML = `
            <div class="card">

                <div class="title">
                    💥 GAME OVER
                </div>

                <div class="description">

                    최종 점수

                    <br>

                    <b
                        style="
                        font-size:36px;
                        color:#ff6797;
                        "
                    >
                        ${Math.floor(score)}
                    </b>

                    <br><br>

                    최고 점수
                    ${bestScore}

                </div>

                <button
                    class="start-button"
                    onclick="startGame()"
                >
                    다시 달리기! 🏃💨
                </button>

            </div>
        `;

    document
        .getElementById("menu")
        .style.display = "flex";
}


// =====================================================
// 배경
// =====================================================

function drawBackground() {

    if (background.complete) {

        ctx.drawImage(
            background,
            0,
            0,
            WIDTH,
            HEIGHT
        );

    } else {

        const gradient =
            ctx.createLinearGradient(
                0,
                0,
                0,
                HEIGHT
            );

        gradient.addColorStop(
            0,
            "#bde9fa"
        );

        gradient.addColorStop(
            1,
            "#d8efc7"
        );

        ctx.fillStyle = gradient;

        ctx.fillRect(
            0,
            0,
            WIDTH,
            HEIGHT
        );
    }


    // 달리는 길

    ctx.fillStyle =
        "rgba(220,205,185,.65)";

    ctx.beginPath();

    ctx.moveTo(230, 300);

    ctx.lineTo(690, 300);

    ctx.lineTo(860, HEIGHT);

    ctx.lineTo(60, HEIGHT);

    ctx.closePath();

    ctx.fill();


    // 레인 구분선

    ctx.strokeStyle =
        "rgba(255,255,255,.75)";

    ctx.lineWidth = 7;

    ctx.beginPath();

    ctx.moveTo(390, 300);

    ctx.lineTo(325, HEIGHT);

    ctx.stroke();

    ctx.beginPath();

    ctx.moveTo(530, 300);

    ctx.lineTo(595, HEIGHT);

    ctx.stroke();
}


// =====================================================
// 장애물
// =====================================================

function drawObstacle(obj) {

    ctx.fillStyle = "#ff779e";

    ctx.strokeStyle = "#67404a";

    ctx.lineWidth = 5;

    ctx.beginPath();

    ctx.roundRect(
        obj.x - 35,
        obj.y - 35,
        70,
        70,
        15
    );

    ctx.fill();

    ctx.stroke();

    ctx.fillStyle = "white";

    ctx.font = "bold 30px Arial";

    ctx.textAlign = "center";

    ctx.textBaseline = "middle";

    ctx.fillText(
        "!",
        obj.x,
        obj.y
    );
}


// =====================================================
// 랜덤박스
// =====================================================

function drawBox(obj) {

    ctx.fillStyle = "#ffd447";

    ctx.strokeStyle = "#9b7430";

    ctx.lineWidth = 5;

    ctx.fillRect(
        obj.x - 32,
        obj.y - 32,
        64,
        64
    );

    ctx.strokeRect(
        obj.x - 32,
        obj.y - 32,
        64,
        64
    );

    ctx.fillStyle = "white";

    ctx.font = "bold 35px Arial";

    ctx.textAlign = "center";

    ctx.textBaseline = "middle";

    ctx.fillText(
        "?",
        obj.x,
        obj.y
    );
}


// =====================================================
// 아이템
// =====================================================

function drawItem(obj) {

    const emojis = {

        giant: "🍄",

        score: "💎",

        shield: "🛡️",

        slow: "🐌",

        speed: "⚡",

        bad: "💀"
    };

    ctx.font = "48px Arial";

    ctx.textAlign = "center";

    ctx.textBaseline = "middle";

    ctx.fillText(
        emojis[obj.item],
        obj.x,
        obj.y
    );
}


// =====================================================
// 플레이어
// =====================================================

function drawPlayer() {

    let image = character1;

    if (
        player.transformation >= 1
    ) {

        image = character3;
    }

    let scale =
        player.giant
        ? 1.55
        : 1;

    let width =
        105 * scale;

    let height =
        120 * scale;

    if (player.sliding) {

        width = 110;

        height = 70;
    }

    ctx.save();

    ctx.translate(
        player.x,
        player.y
    );


    // 변신 뒤돌아보기

    if (player.turning) {

        ctx.rotate(Math.PI);
    }


    if (image.complete) {

        ctx.drawImage(
            image,
            -width / 2,
            -height,
            width,
            height
        );
    }


    // 왕관

    if (
        player.transformation >= 2
    ) {

        ctx.font = "32px Arial";

        ctx.textAlign = "center";

        ctx.fillText(
            "👑",
            0,
            -height - 10
        );
    }


    // 거대화

    if (player.giant) {

        ctx.fillStyle = "#ffb52e";

        ctx.font = "bold 20px Arial";

        ctx.textAlign = "center";

        ctx.fillText(
            "GIANT!",
            0,
            -height - 15
        );
    }


    // 보호막

    if (player.shield) {

        ctx.strokeStyle = "#63dcff";

        ctx.lineWidth = 5;

        ctx.beginPath();

        ctx.arc(
            0,
            -height / 2,
            65,
            0,
            Math.PI * 2
        );

        ctx.stroke();
    }

    ctx.restore();
}


// =====================================================
// 친구
// =====================================================

function drawFriend() {

    const x =
        player.x - 105;

    const y =
        player.y + 5;

    ctx.save();

    ctx.translate(
        x,
        y
    );


    // 점프 백덤블링

    if (player.jumping) {

        player.rotation += 0.28;

        ctx.rotate(
            player.rotation
        );
    }


    if (character2.complete) {

        ctx.drawImage(
            character2,
            -38,
            -48,
            76,
            96
        );
    }

    ctx.restore();
}


// =====================================================
// 파티클
// =====================================================

function createParticles(
    x,
    y,
    color,
    amount
) {

    for (
        let i = 0;
        i < amount;
        i++
    ) {

        particles.push({

            x: x,

            y: y,

            velocityX:
                (Math.random() - 0.5) * 10,

            velocityY:
                (Math.random() - 0.5) * 10,

            life: 35,

            color: color
        });
    }
}


function updateParticles() {

    particles.forEach(
        function(p) {

            p.x += p.velocityX;

            p.y += p.velocityY;

            p.velocityY += 0.25;

            p.life--;
        }
    );

    particles =
        particles.filter(
            function(p) {

                return p.life > 0;
            }
        );
}


function drawParticles() {

    particles.forEach(
        function(p) {

            ctx.globalAlpha =
                p.life / 35;

            ctx.fillStyle =
                p.color;

            ctx.beginPath();

            ctx.arc(
                p.x,
                p.y,
                5,
                0,
                Math.PI * 2
            );

            ctx.fill();
        }
    );

    ctx.globalAlpha = 1;
}


// =====================================================
// 전체 그리기
// =====================================================

function draw() {

    drawBackground();

    objects.forEach(
        function(obj) {

            if (
                obj.type === "obstacle"
            ) {

                drawObstacle(obj);

            } else if (
                obj.type === "box"
            ) {

                drawBox(obj);

            } else {

                drawItem(obj);
            }
        }
    );

    drawFriend();

    drawPlayer();

    drawParticles();
}


// =====================================================
// 게임 루프
// =====================================================

function gameLoop() {

    update();

    draw();

    document
        .getElementById("score")
        .textContent =
        Math.floor(score);

    document
        .getElementById("best")
        .textContent =
        Math.max(
            bestScore,
            Math.floor(score)
        );

    requestAnimationFrame(
        gameLoop
    );
}


gameLoop();

</script>

</body>
</html>
"""


# =========================================================
# 이미지 주소 삽입
# =========================================================

game = game.replace(
    "__CHARACTER1__",
    CHARACTER1
)

game = game.replace(
    "__CHARACTER2__",
    CHARACTER2
)

game = game.replace(
    "__CHARACTER3__",
    CHARACTER3
)

game = game.replace(
    "__BACKGROUND__",
    BACKGROUND
)


# =========================================================
# 실행
# =========================================================

components.html(
    game,
    height=760,
    scrolling=False
)
