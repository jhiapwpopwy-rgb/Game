import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64

st.set_page_config(
    page_title="Chiikawa Run!",
    page_icon="🌸",
    layout="centered"
)

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


st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        180deg,
        #dff6ff 0%,
        #fff0f5 100%
    );
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

.block-container {
    padding-top: 5px !important;
    padding-bottom: 0 !important;
    max-width: 1000px !important;
}
</style>
""", unsafe_allow_html=True)


game = r"""
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
    -webkit-tap-highlight-color: transparent;
}

html,
body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: transparent;
    font-family: Arial, sans-serif;
}

#gameWrap {
    width: 100%;
    display: flex;
    justify-content: center;
}

#game {
    width: min(920px, 100vw);
    position: relative;
}

canvas {
    width: 100%;
    height: auto;
    display: block;
    border-radius: 20px;
}


/* =========================
   HUD
========================= */

.hud {
    position: absolute;
    top: 10px;
    left: 10px;
    right: 10px;

    display: flex;
    justify-content: space-between;

    z-index: 5;
    pointer-events: none;
}

.hudBox {
    background: rgba(255,255,255,.9);
    color: #604850;
    font-weight: 900;
    font-size: 13px;

    padding: 6px 10px;
    border-radius: 13px;

    box-shadow:
        0 3px 8px rgba(0,0,0,.12);
}


/* =========================
   MENU
========================= */

#menu {
    position: absolute;
    inset: 0;

    z-index: 20;

    display: flex;
    justify-content: center;
    align-items: center;

    padding: 12px;

    background: rgba(255,255,255,.18);

    border-radius: 20px;
}

.menuCard {
    width: min(390px, 82%);
    max-height: 82%;

    background: rgba(255,255,255,.97);

    border-radius: 22px;

    padding: 18px 14px;

    text-align: center;

    box-shadow:
        0 10px 25px rgba(60,40,60,.22);

    overflow: hidden;
}

.title {
    color: #5d3f47;
    font-weight: 900;
    font-size: clamp(23px, 6vw, 32px);
    margin-bottom: 9px;
}

.description {
    color: #76666d;
    font-size: clamp(12px, 3.2vw, 16px);
    line-height: 1.38;
    margin-bottom: 12px;
}

.startButton {
    appearance: none;
    -webkit-appearance: none;

    border: none;

    width: 100%;

    padding: 13px 18px;

    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            #ff9abb,
            #ff6497
        );

    color: white;

    font-size: 16px;
    font-weight: 900;

    box-shadow:
        0 5px 0 #d74d79;

    cursor: pointer;

    touch-action: manipulation;
}

.startButton:active {
    transform: translateY(4px);
    box-shadow: none;
}


/* =========================
   조작 버튼
========================= */

.controls {
    position: absolute;

    left: 50%;
    bottom: 8px;

    transform: translateX(-50%);

    display: flex;
    gap: 6px;

    z-index: 15;
}

.ctrl {
    appearance: none;
    -webkit-appearance: none;

    width: 43px;
    height: 39px;

    padding: 0;

    border: 0;
    border-radius: 13px;

    background: rgba(255,255,255,.9);

    color: #5d4b50;

    font-size: 18px;

    box-shadow:
        0 3px 8px rgba(0,0,0,.13);

    touch-action: manipulation;
}

.ctrl:active {
    transform: scale(.93);
}


/* =========================
   모바일
========================= */

@media (max-width: 600px) {

    #game {
        width: 100vw;
    }

    canvas {
        border-radius: 16px;
    }

    #menu {
        padding: 7px;
    }

    .menuCard {
        width: 76%;
        max-height: 78%;
        padding: 14px 12px;
        border-radius: 20px;
    }

    .title {
        font-size: 22px;
        margin-bottom: 7px;
    }

    .description {
        font-size: 12px;
        line-height: 1.3;
        margin-bottom: 9px;
    }

    .startButton {
        padding: 11px 12px;
        font-size: 14px;
    }

    .hud {
        top: 7px;
        left: 7px;
        right: 7px;
    }

    .hudBox {
        font-size: 11px;
        padding: 5px 8px;
    }

    .controls {
        bottom: 6px;
    }

    .ctrl {
        width: 39px;
        height: 36px;
        font-size: 16px;
    }
}

</style>
</head>

<body>

<div id="gameWrap">

<div id="game">

<canvas
    id="canvas"
    width="920"
    height="650">
</canvas>


<div class="hud">

    <div class="hudBox">
        ⭐ <span id="score">0</span>
    </div>

    <div class="hudBox">
        🏆 <span id="best">0</span>
    </div>

    <div class="hudBox">
        🎭 <span id="form">기본</span>
    </div>

</div>


<div id="menu">

    <div class="menuCard">

        <div class="title">
            🌸 CHIIKAWA RUN! 🌸
        </div>

        <div class="description">

            치이카와 친구들과 함께 달려보세요! 🏃

            <br><br>

            ◀ ▶ 이동 · ⬆ 점프 · ⬇ 슬라이드

            <br>

            🎁 랜덤박스를 먹으면
            좋은 아이템 또는 나쁜 아이템 등장!

            <br>

            🍄 커지면 장애물을 부술 수 있어요.

            <br>

            ✨ 점수에 따라 모습이 바뀝니다.

        </div>

        <button
            id="startButton"
            class="startButton"
            type="button"
        >
            START RUN! 🏃
        </button>

    </div>

</div>


<div class="controls">

    <button
        class="ctrl"
        id="leftButton"
        type="button"
    >
        ◀
    </button>

    <button
        class="ctrl"
        id="jumpButton"
        type="button"
    >
        ⬆
    </button>

    <button
        class="ctrl"
        id="rightButton"
        type="button"
    >
        ▶
    </button>

    <button
        class="ctrl"
        id="slideButton"
        type="button"
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
// Canvas
// =====================================================

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;


// =====================================================
// 버튼
// =====================================================

const startButton =
    document.getElementById("startButton");

const leftButton =
    document.getElementById("leftButton");

const rightButton =
    document.getElementById("rightButton");

const jumpButton =
    document.getElementById("jumpButton");

const slideButton =
    document.getElementById("slideButton");


// =====================================================
// 게임 상태
// =====================================================

let running = false;

let score = 0;

let best =
    Number(
        localStorage.getItem(
            "chiikawa_best"
        ) || 0
    );

let speed = 7;

let distance = 0;

let spawnTimer = 40;

let objects = [];

let particles = [];


// =====================================================
// 플레이어
// =====================================================

const lanes = [300, 460, 620];

let player = {
    lane: 1,
    x: 460,
    targetX: 460,

    y: 515,

    vy: 0,

    jumping: false,

    sliding: false,
    slideTimer: 0,

    giant: false,
    giantTimer: 0,

    shield: false,
    shieldTimer: 0,

    form: 0,

    turning: false,
    turnTimer: 0,

    rotation: 0
};


// =====================================================
// START
// =====================================================

function startGame() {

    running = true;

    score = 0;

    speed = 7;

    distance = 0;

    spawnTimer = 40;

    objects = [];

    particles = [];

    player = {
        lane: 1,
        x: 460,
        targetX: 460,

        y: 515,

        vy: 0,

        jumping: false,

        sliding: false,
        slideTimer: 0,

        giant: false,
        giantTimer: 0,

        shield: false,
        shieldTimer: 0,

        form: 0,

        turning: false,
        turnTimer: 0,

        rotation: 0
    };

    document
        .getElementById("menu")
        .style.display = "none";
}


// =====================================================
// 모바일 버튼
// =====================================================

function touchAction(element, action) {

    element.addEventListener(
        "pointerdown",
        function(event) {

            event.preventDefault();

            action();
        }
    );
}

touchAction(
    startButton,
    startGame
);

touchAction(
    leftButton,
    moveLeft
);

touchAction(
    rightButton,
    moveRight
);

touchAction(
    jumpButton,
    jump
);

touchAction(
    slideButton,
    slide
);


// =====================================================
// 이동
// =====================================================

function moveLeft() {

    if (!running)
        return;

    if (player.lane > 0) {

        player.lane--;

        player.targetX =
            lanes[player.lane];
    }
}

function moveRight() {

    if (!running)
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

    if (!running)
        return;

    if (!player.jumping) {

        player.jumping = true;

        player.vy = -18;

        player.rotation = 0;
    }
}


// =====================================================
// 슬라이드
// =====================================================

function slide() {

    if (!running)
        return;

    if (!player.jumping) {

        player.sliding = true;

        player.slideTimer = 38;
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
        Math.floor(
            Math.random() * 3
        );

    const r =
        Math.random();

    let type =
        "obstacle";

    let item = null;


    if (r < 0.45) {

        type = "obstacle";

    } else if (r < 0.70) {

        type = "box";

    } else {

        type = "item";

        const q =
            Math.random();

        if (q < 0.18)
            item = "giant";

        else if (q < 0.36)
            item = "score";

        else if (q < 0.52)
            item = "shield";

        else if (q < 0.68)
            item = "slow";

        else if (q < 0.84)
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
// 아이템
// =====================================================

function getItem(item) {

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

        speed =
            Math.max(
                4,
                speed - 2
            );
    }

    if (item === "speed") {

        score += 250;

        speed =
            Math.min(
                16,
                speed + 1
            );
    }

    if (item === "bad") {

        score =
            Math.max(
                0,
                score - 350
            );

        speed =
            Math.min(
                16,
                speed + 2
            );
    }
}


// =====================================================
// 랜덤박스
// =====================================================

function openBox(obj) {

    const r =
        Math.random();

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


    getItem(item);

    burst(
        obj.x,
        obj.y,
        "#ffd447",
        22
    );
}


// =====================================================
// 충돌
// =====================================================

function hit(playerObj, obj) {

    return (
        playerObj.lane === obj.lane &&
        Math.abs(
            playerObj.y - obj.y
        ) < 70
    );
}


// =====================================================
// 변신
// =====================================================

function transformationCheck() {

    let newForm = 0;

    if (score >= 5000) {

        newForm = 2;

    } else if (score >= 2500) {

        newForm = 1;
    }


    if (
        newForm >
        player.form
    ) {

        player.form =
            newForm;

        player.turning = true;

        player.turnTimer = 120;

        burst(
            player.x,
            player.y - 70,
            "#ff9fc0",
            30
        );
    }


    let text = "기본";

    if (player.form === 1)
        text = "✨ 변신";

    if (player.form === 2)
        text = "👑 최종";


    document
        .getElementById("form")
        .textContent = text;
}


// =====================================================
// UPDATE
// =====================================================

function update() {

    if (!running)
        return;


    distance += speed;

    score += 0.28;

    speed =
        Math.min(
            16,
            7 + distance / 6500
        );


    transformationCheck();


    player.x +=
        (
            player.targetX -
            player.x
        ) * 0.2;


    // 점프

    if (player.jumping) {

        player.vy += 1;

        player.y += player.vy;


        if (player.y >= 515) {

            player.y = 515;

            player.vy = 0;

            player.jumping = false;
        }
    }


    // 슬라이드

    if (player.sliding) {

        player.slideTimer--;

        if (
            player.slideTimer <= 0
        ) {

            player.sliding = false;
        }
    }


    // 거대화

    if (player.giant) {

        player.giantTimer--;

        if (
            player.giantTimer <= 0
        ) {

            player.giant = false;
        }
    }


    // 보호막

    if (player.shield) {

        player.shieldTimer--;

        if (
            player.shieldTimer <= 0
        ) {

            player.shield = false;
        }
    }


    // 변신 뒤돌아보기

    if (player.turning) {

        player.turnTimer--;

        if (
            player.turnTimer <= 0
        ) {

            player.turning = false;
        }
    }


    // 생성

    spawnTimer--;

    if (
        spawnTimer <= 0
    ) {

        spawnObject();

        spawnTimer =
            Math.max(
                28,
                75 - speed * 2
            );
    }


    // 이동

    objects.forEach(
        function(obj) {

            obj.y += speed;
        }
    );


    // 충돌

    for (
        let i = objects.length - 1;
        i >= 0;
        i--
    ) {

        const obj =
            objects[i];


        if (
            !hit(player, obj)
        )
            continue;


        if (
            obj.type === "box"
        ) {

            openBox(obj);

            objects.splice(i, 1);

            continue;
        }


        if (
            obj.type === "item"
        ) {

            getItem(obj.item);

            objects.splice(i, 1);

            continue;
        }


        if (
            obj.type === "obstacle"
        ) {

            if (player.jumping)
                continue;


            if (player.giant) {

                score += 200;

                burst(
                    obj.x,
                    obj.y,
                    "#ff82a8",
                    20
                );

                objects.splice(i, 1);

                continue;
            }


            if (player.shield) {

                player.shield = false;

                objects.splice(i, 1);

                continue;
            }


            gameOver();

            return;
        }
    }


    objects =
        objects.filter(
            function(obj) {

                return obj.y <
                    HEIGHT + 100;
            }
        );


    updateParticles();
}


// =====================================================
// GAME OVER
// =====================================================

function gameOver() {

    running = false;


    const finalScore =
        Math.floor(score);


    if (
        finalScore > best
    ) {

        best =
            finalScore;

        localStorage.setItem(
            "chiikawa_best",
            best
        );
    }


    document
        .getElementById("menu")
        .innerHTML = `
            <div class="menuCard">

                <div class="title">
                    💥 GAME OVER
                </div>

                <div class="description">
                    최종 점수<br>
                    <b
                        style="
                        font-size:34px;
                        color:#ff6797;
                        "
                    >
                        ${finalScore}
                    </b>

                    <br><br>

                    🏆 최고 점수 ${best}
                </div>

                <button
                    id="restartButton"
                    class="startButton"
                    type="button"
                >
                    다시 달리기! 🏃
                </button>

            </div>
        `;


    document
        .getElementById("menu")
        .style.display = "flex";


    document
        .getElementById("restartButton")
        .addEventListener(
            "pointerdown",
            function(event) {

                event.preventDefault();

                startGame();
            }
        );
}


// =====================================================
// BACKGROUND
// =====================================================

function drawBackground() {

    if (
        background.complete &&
        background.naturalWidth > 0
    ) {

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
            "#bfeaff"
        );

        gradient.addColorStop(
            1,
            "#d9efc9"
        );

        ctx.fillStyle =
            gradient;

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

    ctx.moveTo(
        230,
        300
    );

    ctx.lineTo(
        690,
        300
    );

    ctx.lineTo(
        860,
        HEIGHT
    );

    ctx.lineTo(
        60,
        HEIGHT
    );

    ctx.closePath();

    ctx.fill();


    // 레인

    ctx.strokeStyle =
        "rgba(255,255,255,.72)";

    ctx.lineWidth = 7;


    ctx.beginPath();

    ctx.moveTo(
        390,
        300
    );

    ctx.lineTo(
        325,
        HEIGHT
    );

    ctx.stroke();


    ctx.beginPath();

    ctx.moveTo(
        530,
        300
    );

    ctx.lineTo(
        595,
        HEIGHT
    );

    ctx.stroke();
}


// =====================================================
// 장애물
// =====================================================

function drawObstacle(obj) {

    ctx.fillStyle =
        "#ff779e";

    ctx.strokeStyle =
        "#67404a";

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


    ctx.fillStyle =
        "white";

    ctx.font =
        "bold 30px Arial";

    ctx.textAlign =
        "center";

    ctx.textBaseline =
        "middle";


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

    ctx.fillStyle =
        "#ffd447";

    ctx.strokeStyle =
        "#9b7430";

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


    ctx.fillStyle =
        "white";

    ctx.font =
        "bold 35px Arial";

    ctx.textAlign =
        "center";

    ctx.textBaseline =
        "middle";


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

    const icons = {

        giant: "🍄",
        score: "💎",
        shield: "🛡️",
        slow: "🐌",
        speed: "⚡",
        bad: "💀"
    };


    ctx.font =
        "46px Arial";

    ctx.textAlign =
        "center";

    ctx.textBaseline =
        "middle";


    ctx.fillText(
        icons[obj.item],
        obj.x,
        obj.y
    );
}


// =====================================================
// 플레이어
// =====================================================

function drawPlayer() {

    let image =
        character1;


    if (
        player.form >= 1
    ) {

        image =
            character3;
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


    if (player.turning) {

        ctx.rotate(
            Math.PI
        );
    }


    if (
        image.complete &&
        image.naturalWidth > 0
    ) {

        ctx.drawImage(
            image,
            -width / 2,
            -height,
            width,
            height
        );
    }


    if (
        player.form >= 2
    ) {

        ctx.font =
            "30px Arial";

        ctx.textAlign =
            "center";

        ctx.fillText(
            "👑",
            0,
            -height - 8
        );
    }


    if (
        player.giant
    ) {

        ctx.fillStyle =
            "#ffb52e";

        ctx.font =
            "bold 19px Arial";

        ctx.textAlign =
            "center";

        ctx.fillText(
            "GIANT!",
            0,
            -height - 12
        );
    }


    if (
        player.shield
    ) {

        ctx.strokeStyle =
            "#63dcff";

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


    if (
        player.jumping
    ) {

        player.rotation += 0.28;

        ctx.rotate(
            player.rotation
        );
    }


    if (
        character2.complete &&
        character2.naturalWidth > 0
    ) {

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

function burst(
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

            vx:
                (Math.random() - 0.5) * 9,

            vy:
                (Math.random() - 0.5) * 9,

            life: 35,

            color: color
        });
    }
}


function updateParticles() {

    particles.forEach(
        function(p) {

            p.x += p.vx;

            p.y += p.vy;

            p.vy += 0.25;

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
// DRAW
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
// LOOP
// =====================================================

function loop() {

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
            best,
            Math.floor(score)
        );


    requestAnimationFrame(
        loop
    );
}


loop();

</script>

</body>
</html>
"""


# =========================================================
# 이미지 삽입
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
    height=540,
    scrolling=False
)
