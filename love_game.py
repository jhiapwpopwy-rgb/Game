from pathlib import Path
import random
import streamlit as st
from PIL import Image

st.set_page_config(page_title='남친/여친 만들기', page_icon='💗', layout='centered')

SPRITE_PATH = Path('character_assets/sprite.png.PNG')

# 원본 1536x1024 스프라이트에서 실제 캐릭터가 있는 부분만 잘라냅니다.
FACE_BOXES = [
    (305, 6, 412, 105), (414, 3, 518, 104), (523, 4, 629, 106),
    (631, 3, 736, 104), (740, 2, 845, 105), (847, 2, 1058, 104),
    (1062, 2, 1166, 106), (1169, 1, 1269, 96),
]

# 확실하게 분리되는 헤어 위주로 사용합니다.
FEMALE_HAIR = [
    (4, 304, 201, 655),
    (107, 306, 194, 424),
    (194, 307, 304, 428),
    (300, 309, 412, 437),
    (414, 304, 518, 434),
    (519, 430, 627, 654),
]
MALE_HAIR = [
    (521, 303, 629, 435),
    (632, 306, 727, 431),
    (734, 308, 834, 405),
    (841, 306, 940, 400),
    (943, 305, 1049, 396),
    (1051, 309, 1150, 398),
]

# 옷은 각각 하나의 옷이 들어오도록 좁게 잡았습니다.
TOP_BOXES = [
    (0, 650, 100, 745),
    (85, 650, 190, 745),
    (175, 650, 285, 755),
    (390, 650, 500, 790),
    (490, 650, 590, 800),
    (570, 650, 670, 745),
    (665, 650, 760, 750),
    (0, 735, 100, 835),
    (90, 735, 200, 835),
    (190, 735, 290, 835),
    (280, 735, 390, 835),
    (380, 735, 490, 835),
    (480, 735, 580, 835),
    (0, 815, 100, 915),
    (90, 815, 200, 915),
    (190, 815, 290, 915),
    (285, 815, 385, 915),
    (380, 815, 480, 915),
    (475, 815, 575, 915),
    (570, 815, 670, 915),
    (665, 815, 760, 915),
]

BOTTOM_BOXES = [
    (755, 610, 860, 715),
    (850, 610, 955, 715),
    (945, 610, 1055, 715),
    (1050, 610, 1160, 715),
    (1155, 610, 1265, 715),
    (755, 730, 850, 825),
    (850, 730, 945, 825),
    (945, 730, 1050, 825),
    (1050, 730, 1165, 825),
]

SHOE_BOXES = [
    (0, 920, 90, 1010), (70, 920, 160, 1010),
    (145, 920, 235, 1010), (215, 920, 305, 1010),
    (280, 920, 375, 1010), (355, 920, 455, 1010),
    (435, 920, 535, 1010), (500, 920, 610, 1010),
    (560, 920, 665, 1010), (625, 920, 760, 1010),
    (760, 920, 850, 1010), (835, 920, 930, 1010),
]

NAMES = {
    '남친': ['민준','도윤','시우','현우','지훈','준서','태윤','건우','이안','유준'],
    '여친': ['서연','지우','하윤','채원','수아','유나','다은','예린','나연','소윤'],
}
TRAITS = [
    '말은 별로 없는데 은근히 잘 챙겨줌',
    '친해지면 갑자기 말이 많아짐',
    '밥 먹을 때 행복해 보임',
    '시험기간에 같이 공부해 줌',
    '사진 찍는 걸 좋아함',
    '게임을 시작하면 승부욕이 엄청남',
    '평소엔 차분한데 가끔 이상한 짓을 함',
    '칭찬을 받으면 하루 종일 기분이 좋음',
]

st.markdown('''
<style>
.main .block-container {max-width: 620px; padding-top: 1.5rem; padding-bottom: 3rem;}
.title {text-align:center; font-size:2.1rem; font-weight:800; margin-bottom:.2rem;}
.subtitle {text-align:center; color:#777; margin-bottom:1.2rem;}
.card {padding:1rem 1.2rem; border-radius:20px; background:rgba(255,255,255,.8); border:1px solid rgba(0,0,0,.08); margin:.7rem 0;}
.stat {font-size:1.1rem; font-weight:700;}
div.stButton > button {width:100%; border-radius:14px; min-height:3rem; font-weight:700;}
</style>
''', unsafe_allow_html=True)

@st.cache_data

def load_sprite():
    if not SPRITE_PATH.exists():
        st.error(f'이미지 파일이 없습니다: {SPRITE_PATH}')
        st.stop()
    return Image.open(SPRITE_PATH).convert('RGBA')


def crop_tight(sprite, box):
    img = sprite.crop(box)
    alpha = img.getchannel('A')
    bbox = alpha.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img


def resize(img, max_w, max_h):
    img = img.copy()
    img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    return img


def make_character(gender):
    sprite = load_sprite()

    # 기본 몸은 원본의 두 인형 중 하나를 사용합니다.
    body_box = (17, 18, 145, 297) if gender == '여친' else (161, 16, 291, 296)
    body = crop_tight(sprite, body_box)
    face = crop_tight(sprite, random.choice(FACE_BOXES))
    hair = crop_tight(sprite, random.choice(FEMALE_HAIR if gender == '여친' else MALE_HAIR))
    top = crop_tight(sprite, random.choice(TOP_BOXES))
    bottom = crop_tight(sprite, random.choice(BOTTOM_BOXES))
    shoes = crop_tight(sprite, random.choice(SHOE_BOXES))

    canvas = Image.new('RGBA', (420, 620), (255, 255, 255, 0))

    # 몸을 크게 배치
    body = resize(body, 230, 500)
    bx = (420 - body.width) // 2
    by = 55
    canvas.alpha_composite(body, (bx, by))

    # 얼굴은 몸의 머리 위치에 정확히 맞춤
    face = resize(face, 150, 145)
    fx = (420 - face.width) // 2
    fy = by + 18
    canvas.alpha_composite(face, (fx, fy))

    # 머리카락은 얼굴 위에 얹되, 너무 크게 만들지 않음
    hair = resize(hair, 245, 300)
    hx = (420 - hair.width) // 2
    hy = by - 10
    canvas.alpha_composite(hair, (hx, hy))

    # 옷과 하의는 몸 위에 얹음
    top = resize(top, 220, 145)
    tx = (420 - top.width) // 2
    canvas.alpha_composite(top, (tx, by + 225))

    bottom = resize(bottom, 220, 125)
    dx = (420 - bottom.width) // 2
    canvas.alpha_composite(bottom, (dx, by + 340))

    shoes = resize(shoes, 180, 90)
    sx = (420 - shoes.width) // 2
    canvas.alpha_composite(shoes, (sx, by + 430))

    return {
        'image': canvas,
        'name': random.choice(NAMES[gender]),
        'trait': random.choice(TRAITS),
        'liking': random.randint(1, 100),
    }

if 'gender' not in st.session_state:
    st.session_state.gender = None
if 'character' not in st.session_state:
    st.session_state.character = None

st.markdown('<div class="title">💗 남친 / 여친 만들기</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">운명은 랜덤이다. 인간은 왜 이런 것에 설레는가.</div>', unsafe_allow_html=True)

if st.session_state.gender is None:
    st.write('### 누구를 만들어 볼까요?')
    c1, c2 = st.columns(2)
    with c1:
        if st.button('💙 남친 만들기', use_container_width=True):
            st.session_state.gender = '남친'
            st.session_state.character = make_character('남친')
            st.rerun()
    with c2:
        if st.button('💗 여친 만들기', use_container_width=True):
            st.session_state.gender = '여친'
            st.session_state.character = make_character('여친')
            st.rerun()
else:
    char = st.session_state.character
    st.image(char['image'], use_container_width=True)
    st.markdown(
        f'<div class="card"><h2>✨ {char["name"]}</h2>'
        f'<p>{char["trait"]}</p><p class="stat">💘 호감도 {char["liking"]}%</p></div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button('🎲 다시 뽑기', use_container_width=True):
            st.session_state.character = make_character(st.session_state.gender)
            st.rerun()
    with c2:
        if st.button('💞 이 사람과 사귀기', use_container_width=True):
            st.success(f'🎉 축하합니다! {char["name"]}님과 사귀게 되었습니다!')

    st.divider()
    if st.button('🔄 처음으로 돌아가기', use_container_width=True):
        st.session_state.gender = None
        st.session_state.character = None
        st.rerun()
