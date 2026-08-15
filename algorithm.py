import streamlit as st

from components.header import render_header
from components.footer import render_footer
from utils.auth import require_login
from utils.matching import SCORING_TABLE, TIME_OPTIONS


st.set_page_config(
    page_title="매칭 테스트 · 이어질 숙명",
    page_icon="💙",
    layout="wide"
)

render_header(active="test")
require_login()


# =========================================
# 세션 상태
# =========================================

st.session_state.setdefault(
    "answers",
    {}
)

st.session_state.setdefault(
    "q_index",
    0
)


# =========================================
# 질문 정의
# =========================================

QUESTIONS = [

    {
        "key": "q1",
        "question": "Q1. 현재 나의 고민(관심사)은?",
        "options": list(
            SCORING_TABLE["q1"].keys()
        ),
    },

    {
        "key": "q2",
        "question": "Q2. 어떤 멘토/멘티를 만나고 싶나요?",
        "options": list(
            SCORING_TABLE["q2"].keys()
        ),
    },

    {
        "key": "q3",
        "question": "Q3. 나의 성향은?",
        "options": list(
            SCORING_TABLE["q3"].keys()
        ),
    },

    {
        "key": "q4",
        "question": "Q4. 나에게 제일 중요한 것은?",
        "options": list(
            SCORING_TABLE["q4"].keys()
        ),
    },

    {
        "key": "q5",
        "question": "Q5. 멘토링이 가장 편한 시간은?",
        "options": TIME_OPTIONS,
    },
]


# =========================================
# 현재 질문
# =========================================

idx = st.session_state.q_index
total = len(QUESTIONS)


st.title("💙 매칭 테스트")

st.write(
    "나의 관심사와 성향을 바탕으로 "
    "나에게 잘 맞는 송이 유형을 찾아보세요."
)

st.progress(
    idx / total,
    text=f"{idx}/{total} 완료"
)


# =========================================
# 질문 표시
# =========================================

if idx < total:

    q = QUESTIONS[idx]

    with st.container(border=True):

        st.subheader(q["question"])

        current_answer = st.session_state.answers.get(
            q["key"]
        )

        # 기존 답변이 있으면 그 위치를 선택
        default_index = None

        if current_answer in q["options"]:
            default_index = q["options"].index(
                current_answer
            )

        answer = st.radio(
            "선택해주세요",
            q["options"],
            index=default_index,
            key=f"input_{q['key']}",
            label_visibility="collapsed"
        )


    st.write("")


    # =====================================
    # 이전 / 다음
    # =====================================

    col1, col2 = st.columns(2)

    with col1:

        if idx > 0:

            if st.button(
                "⬅ 이전",
                use_container_width=True
            ):

                st.session_state.q_index -= 1
                st.rerun()


    with col2:

        if idx == total - 1:
            button_text = "결과 보기 🎉"
        else:
            button_text = "다음 ➡"


        if st.button(
            button_text,
            type="primary",
            use_container_width=True
        ):

            if answer is None:

                st.warning(
                    "답변을 선택해주세요."
                )

            else:

                # 답변 저장
                st.session_state.answers[
                    q["key"]
                ] = answer

                # 마지막 질문이면 결과 페이지로
                if idx == total - 1:

                    st.switch_page(
                        "pages/Matching_Result.py"
                    )

                else:

                    st.session_state.q_index += 1
                    st.rerun()


# =========================================
# 테스트 완료 상태
# =========================================

else:

    st.success(
        "모든 질문에 답했어요!"
    )

    if st.button(
        "🌸 결과 확인하기",
        type="primary",
        use_container_width=True
    ):

        st.switch_page(
            "pages/Matching_Result.py"
        )


render_footer()
