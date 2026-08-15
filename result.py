import streamlit as st

from components.header import render_header
from components.footer import render_footer
from utils.matching import get_matching_result
from utils.auth import require_login


st.set_page_config(
    page_title="매칭 결과 · 이어질 숙명",
    page_icon="💙",
    layout="wide"
)

render_header(active="test")
require_login()


# =========================================
# 답변 확인
# =========================================

answers = st.session_state.get(
    "answers",
    {}
)


REQUIRED_QUESTIONS = [
    "q1",
    "q2",
    "q3",
    "q4",
    "q5",
]


if not all(
    key in answers
    for key in REQUIRED_QUESTIONS
):

    st.warning(
        "먼저 매칭 테스트를 완료해주세요."
    )

    if st.button(
        "매칭 테스트 하러 가기",
        type="primary"
    ):

        st.switch_page(
            "pages/Matching_Test.py"
        )

    st.stop()


# =========================================
# 유형 분류 알고리즘 실행
# =========================================

result = get_matching_result(
    answers
)

st.session_state.result = result


result_type = result["type"]
emoji = result["emoji"]


# =========================================
# 결과 표시
# =========================================

st.markdown(
    f"""
    <div style="
        text-align:center;
        padding:30px 0;
    ">

        <div style="
            font-size:60px;
        ">
            {emoji}
        </div>

        <h1>
            {result_type}
        </h1>

        <p style="
            font-size:18px;
            color:#666;
        ">
            {result["desc"]}
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================
# 최종 유형
# =========================================

with st.container(border=True):

    st.markdown(
        f"### {emoji} {result['title']}"
    )

    st.write(
        result["desc"]
    )


st.divider()


# =========================================
# 유형별 최종 점수
# =========================================

st.subheader("📊 유형별 점수")


scores = result["scores"]

sorted_scores = sorted(
    scores.items(),
    key=lambda item: item[1],
    reverse=True
)


for type_name, score in sorted_scores:

    type_emoji = {
        "열정송이": "🔥",
        "새싹송이": "🌱",
        "탐구송이": "🔍",
        "소통송이": "💬",
    }[type_name]

    st.markdown(
        f"**{type_emoji} {type_name}** "
        f"— {score:.2f}점"
    )

    st.progress(
        score / 100
    )


st.divider()


# =========================================
# 질문별 점수 상세
# =========================================

with st.expander("🔎 질문별 점수 상세 보기"):

    detail_scores = result[
        "detail_scores"
    ]

    question_names = {
        "q1": "Q1. 현재 나의 고민(관심사)은?",
        "q2": "Q2. 어떤 멘토/멘티를 만나고 싶나요?",
        "q3": "Q3. 나의 성향은?",
        "q4": "Q4. 나에게 제일 중요한 것은?",
    }


    for question_key in [
        "q1",
        "q2",
        "q3",
        "q4",
    ]:

        st.markdown(
            f"#### {question_names[question_key]}"
        )

        question_scores = detail_scores.get(
            question_key,
            {}
        )

        for type_name in [
            "열정송이",
            "새싹송이",
            "탐구송이",
            "소통송이",
        ]:

            data = question_scores.get(
                type_name
            )

            if data:

                st.write(
                    f"{type_name}: "
                    f"원점수 {data['raw']}점 "
                    f"→ 가중점수 "
                    f"{data['weighted']:.2f}점"
                )


st.divider()


# =========================================
# Q5 시간 정보
# =========================================

st.subheader("🕐 멘토링 가능 시간")

st.info(
    f"선택한 시간: **{result['available_time']}**"
)

st.caption(
    "멘토링 가능 시간은 유형 분류에는 반영되지 않으며, "
    "추후 멘토·멘티 추천 시 활용됩니다."
)


# =========================================
# 다시 테스트
# =========================================

st.divider()

if st.button(
    "↻ 다시 테스트하기",
    use_container_width=True
):

    st.session_state.answers = {}
    st.session_state.q_index = 0

    # 질문 위젯 초기화
    for key in list(
        st.session_state.keys()
    ):

        if key.startswith("input_"):
            del st.session_state[key]

    st.rerun()


render_footer()
