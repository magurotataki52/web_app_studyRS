import streamlit as st
from datetime import datetime, timedelta

def backToTop():
    st.session_state.movePageTo = {"directory":"contents/top.py","title":"トップ"}

def goToSubjectEdit():
    st.session_state.movePageTo = {"directory":"contents/subject.py","title":"教科設定"}

def complete():
    st.session_state.movePageTo = {"directory":"contents/record_complete.py","title":"記録完了"}

def addSchedule(date,subject,title,time):
    datetime_str = date.strftime("%Y-%m-%d")
    st.session_state.schedules.append({"date":datetime_str,"subject":subject,"title":f"{title} ({time}分)","time":time})

def record(date,subject,title,time):
    st.session_state.records.append({"date":date,"subject":subject,"title":title,"time":time})

def recordSubmit(date,subject,title,time,auto_scheduler):
    record(date,subject,title,time)
    if auto_scheduler:
        first_review = date + timedelta(days=1)
        first_time = round(time / (60 / 10))
        second_review = date + timedelta(days=7)
        second_time = round(time / (60 / 5))
        third_review = date + timedelta(days=30)
        third_time = round(time / (60 / 3))
        addSchedule(first_review,subject,title,first_time)
        addSchedule(second_review,subject,title,second_time)
        addSchedule(third_review,subject,title,third_time)
    complete()


st.button("<<トップに戻る", on_click=backToTop)   
st.header("記録")
st.write("")

dt_today = datetime.today()
min_date = datetime(2000, 1, 1)
date_input = st.date_input('日付', dt_today, min_value=min_date, max_value=dt_today)
col1, col2 = st.columns(2)

sbjName_list = ["設定しない"]

for i in range(len(st.session_state.subjects)):
    sbjName_list.append(st.session_state.subjects[i]["name"])

subject_input = col1.selectbox('教科', sbjName_list)
add_subject_btn = col2.button("教科を設定", on_click=goToSubjectEdit)
time_input = st.number_input("時間(分)", step=5, min_value=0, max_value=720, value=st.session_state.record_Initial_value["time"])
title_input = st.text_input("タイトル")
auto_schedule = st.checkbox("自動で復習予定を作成する",value=True)
submit_btn = st.button("確定", type="primary", use_container_width=True,on_click=recordSubmit,args=[date_input,subject_input,title_input,time_input,auto_schedule])
