import random
import requests
import streamlit as st

# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="Movie Match",
    page_icon="🍿",
    layout="wide"
)

API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# TMDB 장르 ID
GENRES = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Science Fiction": 878,
    "Thriller": 53,
    "War": 10752,
}

# =========================================================
# TMDB API 함수
# =========================================================

def tmdb_get(endpoint, params=None):
    """TMDB API 요청"""
    if params is None:
        params = {}

    params["api_key"] = API_KEY
    params["language"] = "ko-KR"

    try:
        response = requests.get(
            BASE_URL + endpoint,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_movies_by_genre(genre_id, exclude_ids=None):
    """특정 장르에서 인기 있고 평점이 괜찮은 영화 가져오기"""

    if exclude_ids is None:
        exclude_ids = []

    data = tmdb_get(
        "/discover/movie",
        {
            "with_genres": genre_id,
            "sort_by": "popularity.desc",
            "vote_count.gte": 500,
            "vote_average.gte": 6.5,
            "include_adult": "false",
            "page": random.randint(1, 5),
            "region": "KR"
        }
    )

    if not data:
        return []

    movies = []

    for movie in data.get("results", []):
        if movie["id"] not in exclude_ids:
            if movie.get("poster_path"):
                movies.append(movie)

    return movies


def get_random_movie(genre_ids, exclude_ids=None):
    """여러 장르 중 하나를 골라 영화 가져오기"""

    if exclude_ids is None:
        exclude_ids = []

    random.shuffle(genre_ids)

    for genre_id in genre_ids:
        movies = get_movies_by_genre(
            genre_id,
            exclude_ids
        )

        if movies:
            return random.choice(movies)

    return None


def get_recommendations(scores):
    """최종 취향 점수를 바탕으로 영화 추천"""

    sorted_genres = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    selected_genres = [
        GENRES[genre]
        for genre, score in sorted_genres[:3]
        if score > 0
    ]

    if not selected_genres:
        selected_genres = [
            GENRES["Drama"],
            GENRES["Science Fiction"],
            GENRES["Thriller"]
        ]

    movies = []

    for genre_id in selected_genres:
        data = tmdb_get(
            "/discover/movie",
            {
                "with_genres": genre_id,
                "sort_by": "vote_average.desc",
                "vote_count.gte": 1000,
                "vote_average.gte": 7.0,
                "include_adult": "false",
                "page": 1,
                "region": "KR"
            }
        )

        if data:
            for movie in data.get("results", []):
                if (
                    movie.get("poster_path")
                    and movie["id"] not in [m["id"] for m in movies]
                ):
                    movies.append(movie)

    random.shuffle(movies)

    return movies[:5]


# =========================================================
# 세션 상태
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "survey"

if "survey_answers" not in st.session_state:
    st.session_state.survey_answers = {}

if "scores" not in st.session_state:
    st.session_state.scores = {
        genre: 0 for genre in GENRES
    }

if "battle_round" not in st.session_state:
    st.session_state.battle_round = 0

if "battle_movies" not in st.session_state:
    st.session_state.battle_movies = None

if "battle_history" not in st.session_state:
    st.session_state.battle_history = []

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 18px;
        margin-bottom: 35px;
    }

    .question {
        font-size: 24px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    .movie-title {
        font-size: 24px;
        font-weight: 700;
        text-align: center;
        margin-top: 10px;
    }

    .movie-info {
        text-align: center;
        color: #777;
    }

    .result-title {
        font-size: 32px;
        font-weight: 800;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🍿 Movie Match</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">당신의 영화 취향을 찾아드립니다.</div>',
    unsafe_allow_html=True
)


# =========================================================
# 1. 설문
# =========================================================

if st.session_state.page == "survey":

    st.progress(0.2)

    st.markdown("## 🎬 먼저 당신의 취향을 알아볼게요")
    st.write("각 질문에서 더 끌리는 쪽을 골라주세요.")

    questions = [
        {
            "question": "1. 어떤 영화가 더 끌리나요?",
            "left": "🚀 상상할 수 없는 세계와 미래",
            "right": "🎭 현실에서 일어날 법한 이야기",
            "left_genres": ["Science Fiction", "Fantasy"],
            "right_genres": ["Drama", "Crime"]
        },
        {
            "question": "2. 영화를 볼 때 가장 중요한 것은?",
            "left": "💥 속도감과 액션",
            "right": "🧠 탄탄한 이야기와 반전",
            "left_genres": ["Action", "Adventure"],
            "right_genres": ["Mystery", "Thriller"]
        },
        {
            "question": "3. 어떤 분위기가 더 좋아요?",
            "left": "😂 가볍고 웃긴 분위기",
            "right": "😭 감정적으로 몰입되는 분위기",
            "left_genres": ["Comedy"],
            "right_genres": ["Drama", "Romance"]
        },
        {
            "question": "4. 어떤 이야기가 더 재미있나요?",
            "left": "🕵️ 범죄와 미스터리",
            "right": "❤️ 사랑과 인간관계",
            "left_genres": ["Crime", "Mystery"],
            "right_genres": ["Romance", "Drama"]
        },
        {
            "question": "5. 영화에서 원하는 것은?",
            "left": "🌌 현실에서 벗어나는 경험",
            "right": "🌎 현실적인 인간 이야기",
            "left_genres": ["Fantasy", "Science Fiction"],
            "right_genres": ["Drama", "History"]
        },
        {
            "question": "6. 어느 쪽이 더 끌리나요?",
            "left": "😱 긴장되고 무서운 영화",
            "right": "😊 따뜻하고 편안한 영화",
            "left_genres": ["Horror", "Thriller"],
            "right_genres": ["Family", "Comedy"]
        }
    ]

    answers = {}

    for i, q in enumerate(questions):

        st.markdown(
            f'<div class="question">{q["question"]}</div>',
            unsafe_allow_html=True
        )

        answer = st.radio(
            "선택",
            [
                q["left"],
                q["right"]
            ],
            horizontal=True,
            key=f"question_{i}",
            label_visibility="collapsed"
        )

        answers[i] = {
            "answer": answer,
            "question": q
        }

    st.write("")

    if st.button(
        "🎬 다음: 영화 대결 시작하기",
        use_container_width=True,
        type="primary"
    ):

        # 점수 초기화
        scores = {
            genre: 0 for genre in GENRES
        }

        # 설문 점수 계산
        for item in answers.values():

            q = item["question"]

            if item["answer"] == q["left"]:
                selected = q["left_genres"]
            else:
                selected = q["right_genres"]

            for genre in selected:
                scores[genre] += 1

        st.session_state.scores = scores
        st.session_state.survey_answers = answers
        st.session_state.page = "battle"

        st.rerun()


# =========================================================
# 2. 영화 A/B 대결
# =========================================================

elif st.session_state.page == "battle":

    round_number = st.session_state.battle_round

    st.progress(
        0.2 + (round_number / 7) * 0.6
    )

    st.markdown("## ⚔️ Movie Battle")
    st.write(
        f"### ROUND {round_number + 1} / 5"
    )

    # 영화가 아직 없으면 생성
    if st.session_state.battle_movies is None:

        sorted_genres = sorted(
            st.session_state.scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_genres = [
            GENRES[g]
            for g, score in sorted_genres[:4]
            if score > 0
        ]

        if not top_genres:
            top_genres = [
                GENRES["Drama"],
                GENRES["Action"]
            ]

        movie_a = get_random_movie(top_genres)

        exclude = []

        if movie_a:
            exclude.append(movie_a["id"])

        movie_b = get_random_movie(
            top_genres,
            exclude
        )

        if movie_a and movie_b:
            st.session_state.battle_movies = [
                movie_a,
                movie_b
            ]

    movies = st.session_state.battle_movies

    if movies:

        col1, col2 = st.columns(2)

        for idx, movie in enumerate(movies):

            with [col1, col2][idx]:

                st.image(
                    IMAGE_BASE_URL + movie["poster_path"],
                    use_container_width=True
                )

                st.markdown(
                    f'<div class="movie-title">'
                    f'{movie.get("title", "제목 없음")}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                year = (
                    movie.get("release_date", "")[:4]
                    if movie.get("release_date")
                    else "연도 정보 없음"
                )

                st.markdown(
                    f'<div class="movie-info">'
                    f'{year} · ⭐ {movie.get("vote_average", 0):.1f}'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.write("")

        st.markdown(
            "<h3 style='text-align:center;'>"
            "어느 영화가 더 보고 싶나요?"
            "</h3>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                f"🍿 {movies[0]['title']}",
                use_container_width=True
            ):

                st.session_state.battle_history.append(
                    movies[0]["id"]
                )

                st.session_state.battle_round += 1
                st.session_state.battle_movies = None

                if st.session_state.battle_round >= 5:
                    st.session_state.page = "result"

                st.rerun()

        with col2:
            if st.button(
                f"🍿 {movies[1]['title']}",
                use_container_width=True
            ):

                st.session_state.battle_history.append(
                    movies[1]["id"]
                )

                st.session_state.battle_round += 1
                st.session_state.battle_movies = None

                if st.session_state.battle_round >= 5:
                    st.session_state.page = "result"

                st.rerun()

    else:

        st.error(
            "영화 정보를 불러오지 못했습니다. "
            "TMDB API 키와 인터넷 연결을 확인해주세요."
        )


# =========================================================
# 3. 결과
# =========================================================

elif st.session_state.page == "result":

    st.progress(1.0)

    st.markdown("## 🧠 당신의 영화 취향 분석")

    scores = st.session_state.scores

    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # 상위 장르
    top_three = sorted_scores[:3]

    st.write("### 🎭 선호 장르")

    for genre, score in sorted_scores:

        if score > 0:

            percentage = int(
                (score / max(1, max(scores.values()))) * 100
            )

            st.write(f"**{genre}**")
            st.progress(percentage / 100)

    # 취향 설명
    top_genre = top_three[0][0]

    descriptions = {
        "Action": "속도감 있고 강렬한 장면이 있는 영화를 좋아하는 편이에요.",
        "Adventure": "새로운 세계와 모험을 떠나는 이야기에 끌리는 편이에요.",
        "Comedy": "가볍고 유쾌하게 즐길 수 있는 영화를 좋아하는 편이에요.",
        "Crime": "범죄 사건과 인물들의 심리를 따라가는 이야기를 좋아하는 편이에요.",
        "Drama": "인물의 감정과 관계를 깊게 다루는 영화에 끌리는 편이에요.",
        "Fantasy": "현실에서는 경험하기 어려운 세계와 설정을 좋아하는 편이에요.",
        "Horror": "긴장감과 공포를 즐기는 편이에요.",
        "Mystery": "숨겨진 단서와 반전을 찾아가는 영화를 좋아하는 편이에요.",
        "Romance": "인물들의 관계와 감정 변화에 관심이 많은 편이에요.",
        "Science Fiction": "과학적 상상력과 미래적인 설정을 좋아하는 편이에요.",
        "Thriller": "긴장감 있고 몰입도 높은 이야기를 좋아하는 편이에요.",
        "History": "역사적 배경과 실제 사건을 다룬 이야기에 관심이 있는 편이에요.",
        "Family": "따뜻하고 편안하게 볼 수 있는 영화를 좋아하는 편이에요."
    }

    st.markdown(
        '<div class="result-title">🎯 당신의 영화 취향</div>',
        unsafe_allow_html=True
    )

    st.info(
        descriptions.get(
            top_genre,
            "다양한 장르의 영화를 즐기는 편이에요."
        )
    )

    # 추천 영화
    st.markdown("## 🍿 당신에게 추천하는 영화")

    if not st.session_state.recommendations:

        with st.spinner("취향에 맞는 영화를 찾는 중..."):

            st.session_state.recommendations = (
                get_recommendations(scores)
            )

    recommendations = st.session_state.recommendations

    if recommendations:

        cols = st.columns(5)

        for i, movie in enumerate(recommendations):

            with cols[i]:

                st.image(
                    IMAGE_BASE_URL + movie["poster_path"],
                    use_container_width=True
                )

                st.markdown(
                    f"**{movie.get('title', '제목 없음')}**"
                )

                st.caption(
                    f"⭐ {movie.get('vote_average', 0):.1f}"
                )

                release_date = movie.get(
                    "release_date",
                    ""
                )

                if release_date:
                    st.caption(
                        release_date[:4]
                    )

    else:

        st.warning(
            "추천 영화를 불러오지 못했습니다."
        )

    st.write("")
    st.write("")

    if st.button(
        "🔄 처음부터 다시 하기",
        use_container_width=True
    ):

        st.session_state.page = "survey"
        st.session_state.survey_answers = {}
        st.session_state.scores = {
            genre: 0 for genre in GENRES
        }
        st.session_state.battle_round = 0
        st.session_state.battle_movies = None
        st.session_state.battle_history = []
        st.session_state.recommendations = []

        st.rerun()


# =========================================================
# Footer
# =========================================================

st.markdown("---")

st.caption(
    "Movie data and images provided by TMDB. "
    "This product uses the TMDB API but is not endorsed or certified by TMDB."
)
