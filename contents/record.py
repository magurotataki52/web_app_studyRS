import streamlit as st
from datetime import datetime

def backToTop():
    st.session_state.movePageTo = {"directory":"contents/top.py","title":"トップ"}

def goToSubjectEdit():
    st.session_state.movePageTo = {"directory":"contents/subject.py","title":"教科設定"}

st.button("<<トップに戻る", on_click=backToTop)   
st.header("直接記録")
st.write("")

dt_today = datetime.today()
min_date = datetime(2000, 1, 1)
date_input = st.date_input('日付', dt_today, min_value=min_date, max_value=dt_today)
col1, col2 = st.columns(2)

sbjName_list = ["設定しない"]

for i in range(len(st.session_state.subjects)):
    sbjName_list.append(st.session_state.subjects[i]["name"])

print(sbjName_list)
subject_input = col1.selectbox('教科', sbjName_list)
add_subject_btn = col2.button("教科を設定", on_click=goToSubjectEdit)
time_input = st.number_input("時間(分)", step=5, min_value=0, max_value=720)
auto_schedule = st.checkbox("自動で復習予定を作成する",value=True)
submit_btn = st.button("確定", type="primary", use_container_width=True)
