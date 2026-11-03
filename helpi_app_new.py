import streamlit as st
from openai import OpenAI

# ---------------------------
# HELPI | 학생 건강정보 챗봇
# ---------------------------
st.set_page_config(
    page_title="HELPI · 학생 건강 도우미",
    page_icon="🩷",
    layout="centered",
)

# 귀여운 파스텔 UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&family=Pretendard:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }
.stApp {
    background: linear-gradient(180deg, #fff5fa 0%, #f5fffc 52%, #fffafd 100%);
}
.block-container { max-width: 850px; padding-top: 1.5rem; padding-bottom: 2rem; }
.helpi-header {
    background: linear-gradient(135deg, #ffd9ec, #d9f7ef);
    border: 1px solid #f7cce3; border-radius: 26px;
    padding: 22px 20px; text-align: center; margin-bottom: 16px;
}
.helpi-logo { font-family: 'Jua', sans-serif; font-size: 42px; color: #df5b9c; letter-spacing: 1px; }
.helpi-sub { color: #6e6670; font-size: 15px; margin-top: 4px; }
.small-card {
    background: rgba(255,255,255,.86); border: 1px solid #f5d9e8;
    border-radius: 18px; padding: 14px 16px; margin: 8px 0;
}
div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,.78);
    border: 1px solid #f4dfeb; border-radius: 18px; padding: 8px 12px;
}
.stButton button {
    border-radius: 16px !important; border: 1px solid #f3cde2 !important;
    background: #fff !important; color: #a84b7c !important; font-weight: 600 !important;
}
.stButton button:hover { background: #fff0f7 !important; border-color: #eaa8cd !important; }
footer {visibility: hidden;}
.helpi-footer { text-align:center; color:#c06a98; padding: 20px 0 6px; font-family:'Jua',sans-serif; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="helpi-header">
  <div style="font-size:34px">🐰🩺</div>
  <div class="helpi-logo">HELPI</div>
  <div class="helpi-sub">학생들을 위한 귀여운 건강정보 도우미 💗</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="small-card">
<b>💬 어디가 불편한가요?</b><br>
증상을 체크할 필요 없이, 지금 느끼는 불편함을 편하게 문장으로 적어 주세요.
정확히 모르겠다면 아래 시작 문구를 눌러도 돼요!
</div>
""", unsafe_allow_html=True)

# API key: Streamlit Secrets에서만 읽기
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("API 키 설정이 필요해요. Streamlit의 Settings → Secrets에 OPENAI_API_KEY를 등록해 주세요.")
    st.code('OPENAI_API_KEY = "여기에_본인의_API_키"', language="toml")
    st.stop()

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
너는 HELPI라는 한국어 학생용 건강정보 안내 챗봇이다. 따뜻하고 귀여운 말투를 쓰되, 의료정보는 정확하고 신중하게 전달한다.
대상은 중·고등학생을 포함한 미성년 사용자다.

핵심 원칙:
- 진단하거나 특정 질환이라고 확정하지 않는다. 증상과 연관될 수 있는 여러 가능성을 조심스럽게 설명하고, 증상만으로 구분이 어려움을 명시한다.
- 사용자의 증상을 자연어로 듣고 필요할 때 한 번에 1~3개의 짧은 추가 질문을 한다. 증상을 체크리스트로만 강요하지 않는다.
- 흔한 학생 증상(두통, 복통, 메스꺼움, 감기 증상, 피로, 어지러움, 생리 관련 불편 등)을 이해하기 쉬운 말로 다룬다.
- 사용자가 원하거나 증상 정보가 충분하면 답변을 아래 구성으로 제공한다:
  1) 지금 말해준 증상 요약
  2) 관련 가능성이 있는 질환/원인 2~4개 (가능성이라고 명시, 확률 순위나 확정 표현 금지)
  3) 도움이 될 수 있는 음식·수분·생활관리 구체 예시
  4) 증상을 악화시킬 수 있어 조심할 음식/습관 (모두에게 금지라고 말하지 말고 개인차 명시)
  5) 약 관련 일반 정보: 특정 제품의 구매/복용을 지시하거나 용량·복용 간격을 정하지 않는다. 약국/편의점 판매 여부도 최신 확인 없이 단정하지 않는다. 약사·보호자와 상담하도록 안내하고, 중복 성분·알레르기·기저질환·복용 중 약에 주의하라고 한다.
  6) 병원/보호자에게 도움을 요청해야 하는 기준
- 음식은 '치료 음식'처럼 단정하지 않는다. 균형 식사와 증상 완화에 도움이 될 수 있는 정도로 표현한다.
- 위험 신호가 있으면 음식/약 추천보다 안전 안내를 우선한다. 갑작스럽고 매우 심한 두통, 호흡곤란, 의식 혼란/실신, 심한 흉통, 심한 복통, 지속적인 구토, 탈수 징후, 고열과 심한 상태 악화, 알레르기 반응으로 입술/혀/목이 붓거나 숨쉬기 어려움 등을 언급하면 즉시 주변 어른에게 알리고 119 또는 응급진료를 받도록 안내한다.
- 미성년 사용자는 증상이 심하거나 지속되면 보호자, 학교 보건교사, 의료진에게 알리도록 권한다.
- 심리적 고통 관련 질문도 따뜻하게 응답하고 믿을 수 있는 어른/상담자에게 연결한다.
- 개인정보(실명, 주소, 학교명, 전화번호 등)를 요청하지 않는다. 사용자가 입력하지 않도록 상기한다.
- 응답은 한국어, 친근하고 간결한 톤, 적당한 이모지. 의학적 면책을 매 답변마다 길게 반복하지 말고, 필요할 때 짧게 표시한다.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# 처음 시작할 수 있는 말풍선 예시
st.markdown("#### 🌷 이런 말로 시작해도 좋아요")
suggestions = [
    "오늘 아침부터 머리가 아프고 속이 울렁거려요.",
    "배가 아픈데 어디가 아픈지 잘 모르겠어요.",
    "시험기간만 되면 너무 피곤하고 어지러워요.",
    "목이 따갑고 기침이 나요.",
    "학생들이 흔히 겪는 증상부터 질문해 주세요.",
    "생리할 때 배가 아픈데 관리법이 궁금해요.",
]
cols = st.columns(2)
for idx, text in enumerate(suggestions):
    with cols[idx % 2]:
        if st.button(text, key=f"suggest_{idx}", use_container_width=True):
            st.session_state.pending_prompt = text

# 대화 초기화
with st.sidebar:
    st.markdown("## 🐰 HELPI")
    st.caption("학생 건강정보 도우미")
    if st.button("🧹 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("pending_prompt", None)
        st.rerun()
    st.markdown("---")
    st.markdown("### 🔒 개인정보 안내")
    st.caption("대화 내용은 답변을 위해 AI API 제공자에게 전송될 수 있어요. 이름·학교·주소 등 식별정보나 민감한 개인정보는 입력하지 마세요. 이 앱은 의료진의 진료를 대신하지 않아요.")

# 이전 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🐰" if msg["role"] == "assistant" else "💬"):
        st.markdown(msg["content"])

prompt = st.chat_input("예: 점심 먹고 배가 아프고 메스꺼워요…")
if not prompt and "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="💬"):
        st.markdown(prompt)

    # 대화 길이를 제한해 토큰 및 비용을 관리
    history = st.session_state.messages[-14:]
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend({"role": m["role"], "content": m["content"]} for m in history)

    with st.chat_message("assistant", avatar="🐰"):
        with st.spinner("헬피가 내용을 살펴보고 있어요… 💗"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=api_messages,
                    temperature=0.3,
                    max_tokens=900,
                )
                answer = response.choices[0].message.content or "답변을 만들지 못했어요. 다시 입력해 주세요."
                st.markdown(answer)
            except Exception as e:
                answer = "앗, 답변을 불러오지 못했어요. API 키와 사용량 한도, 인터넷 연결을 확인해 주세요."
                st.error(answer)
                # 사용자에게 내부 예외나 API 세부정보를 노출하지 않음

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.markdown("""
<div class="helpi-footer">
  🩷 HELPI · 건강한 학교생활을 응원해요 🩷<br>
  <span style="font-family:'Pretendard',sans-serif;font-size:11px;color:#9a8b94">
  건강정보 참고용 · 진단 및 치료를 대신하지 않습니다
  </span>
</div>
""", unsafe_allow_html=True)
