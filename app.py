import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILE_NAME = "schedule.csv"

# 파일 없으면 생성
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["date", "time", "task"])
    df.to_csv(FILE_NAME, index=False)

# 데이터 불러오기
df = pd.read_csv(FILE_NAME)

st.title("📅 스케줄 관리 앱")

# -----------------------
# 일정 추가
# -----------------------
st.header("일정 추가")

col1, col2 = st.columns(2)

with col1:
    date = st.date_input("날짜")

with col2:
    time = st.time_input("시간")

task = st.text_input("할 일")

if st.button("추가"):
    if task.strip() != "":
        new_data = pd.DataFrame([{
            "date": str(date),
            "time": str(time),
            "task": task
        }])

        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)

        st.success("일정이 추가되었습니다!")
    else:
        st.warning("할 일을 입력하세요.")

# -----------------------
# 일정 보기
# -----------------------
st.header("일정 목록")

if len(df) > 0:
    df_sorted = df.sort_values(by=["date", "time"])
    st.dataframe(df_sorted, use_container_width=True)

    # -----------------------
    # 일정 삭제
    # -----------------------
    st.header("일정 삭제")

    delete_index = st.number_input(
        "삭제할 일정 번호(index)",
        min_value=0,
        max_value=len(df_sorted)-1,
        step=1
    )

    if st.button("삭제"):
        df_sorted = df_sorted.drop(delete_index)
        df_sorted.to_csv(FILE_NAME, index=False)

        st.success("삭제되었습니다!")
else:
    st.info("등록된 일정이 없습니다.")
