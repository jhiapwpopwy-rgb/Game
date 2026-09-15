import streamlit as st
from openai import OpenAI
import re

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="AI 조언 연습장",
    page_icon="💗",
    layout="centered"
)

# -----------------------------
# OpenAI API
# -----------------------------
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OPENAI_API_KEY가 설정되지 않았어요.")
    st.info("Streamlit Cloud → Settings → Secrets에서 API Key를 입력해주세요.")
    st.stop()

client = OpenAI(api_key=api_key)

# -----------------------------
# 캐릭터
# -----------------------------
CHARACTERS = {
    "sad": {
        "face": "🥺",
        "name": "토닥토닥",
        "message": "괜찮아. 오늘 조금 힘들었나 봐. 내가 옆에 있을게."
    },
    "angry": {
        "face": "😤",
        "name": "씩씩이",
        "message": "그럴 만했어. 일단 숨 한번 크게 쉬자!"
    },
    "anxious": {
        "face": "🥹",
        "name": "콩닥이",
        "message": "걱정이 많았구나. 하나씩 천천히 생각해보자."
    },
    "tired": {
        "face": "😮‍💨",
        "name": "몽글이",
        "message": "많이 지쳤겠다. 잠깐 쉬어가도 괜찮아."
    },
    "happy": {
        "face": "😊",
        "name": "방긋이",
        "message": "조금씩 나아지고 있는 것 같아! 잘하고 있어."
    }
}

# -----------------------------
# 제목
# -----------------------------
st.title("💗 AI 조언 연습장")
st.caption("고민을 적어주면 귀여운 친구가 함께 고민해줘요!")

st.divider()

# -----------------------------
# 고민 입력
# -----------------------------
problem = st.text_area(
    "💭 무슨 고민이 있나요?",
    placeholder="예: 친구랑 싸웠는데 먼저 연락해야 할지 모르겠어...",
    height=160
)

style = st.selectbox(
    "🌷 어떤 조언을 받고 싶나요?",
    [
        "따뜻하고 공감하는 조언",
        "친구처럼 편한 조언",
        "현실적이고 솔직한 조언",
        "논리적으로 정리해주는 조언",
        "짧고 핵심적인 조언"
    ]
)

# -----------------------------
# 조언 받기
# -----------------------------
if st.button("💌 조언 받기", use_container_width=True):

    if not problem.strip():
        st.warning("고민을 먼저 적어주세요! 🥺")
        st.stop()

    system_prompt = f"""
너는 사용자의 고민을 들어주는 따뜻한 AI 조언자다.

사용자의 고민을 읽고 감정과 상황을 파악한 뒤
현실적으로 도움이 되는 조언을 해준다.

조언 스타일:
{style}

답변은 반드시 다음 형식으로 작성한다.

MOOD: 하나만 선택
sad / angry / anxious / tired / happy

ADVICE:
사용자에게 해줄 조언

규칙:
- 한국어로 자연스럽게 작성한다.
- 사용자의 감정을 무시하거나 판단하지 않는다.
- 지나치게 뻔한 위로만 하지 않는다.
- 실제로 해볼 수 있는 방법을 제시한다.
- 너무 길지 않게 작성한다.
- MOOD에는 반드시 위 5개 중 하나만 적는다.
"""

    user_prompt = f"""
사용자의 고민:

{problem}
"""

    with st.spinner("토닥토닥 친구가 고민을 읽고 있어요... 🐰"):

        try:
            response = client.responses.create(
                model="gpt-5.4-nano",
                instructions=system_prompt,
                input=user_prompt
            )

            result = response.output_text.strip()

            # -----------------------------
            # 감정 상태 추출
            # -----------------------------
            mood_match = re.search(
                r"MOOD:\s*(sad|angry|anxious|tired|happy)",
                result,
                re.IGNORECASE
            )

            if mood_match:
                mood = mood_match.group(1).lower()
            else:
                mood = "sad"

            # -----------------------------
            # 조언 내용만 추출
            # -----------------------------
            advice_match = re.search(
                r"ADVICE:\s*(.*)",
                result,
                re.IGNORECASE | re.DOTALL
            )

            if advice_match:
                advice = advice_match.group(1).strip()
            else:
                advice = result

            character = CHARACTERS[mood]

            st.divider()

            # -----------------------------
            # 캐릭터
            # -----------------------------
            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding:25px 10px 15px 10px;
                ">
                    <div style="
                        font-size:90px;
                        line-height:1.2;
                    ">
                        {character["face"]}
                    </div>

                    <h3 style="margin-top:10px;">
                        {character["name"]}
                    </h3>

                    <p style="
                        font-size:16px;
                        margin-top:5px;
                    ">
                        {character["message"]}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # -----------------------------
            # AI 조언
            # -----------------------------
            st.subheader("💬 내가 해줄 말")

            st.markdown(
                f"""
                <div style="
                    padding:20px;
                    border-radius:18px;
                    background-color:#f7f7f7;
                    line-height:1.7;
                    font-size:16px;
                ">
                    {advice.replace(chr(10), "<br>")}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()

            st.caption("💗 혼자 끙끙 앓지 말고, 하나씩 해결해봐요.")

        except Exception as e:
            st.error("조언을 가져오는 중 문제가 발생했어요.")
            st.code(str(e))
