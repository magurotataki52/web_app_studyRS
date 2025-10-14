import streamlit as st
import math
import time

if "study_time" not in st.session_state:
    st.session_state.study_time = 5
if "rest_time" not in st.session_state:
    st.session_state.rest_time = 5
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "pause_time" not in st.session_state:
    st.session_state.pause_time = 0
if "remaining_time" not in st.session_state:
    st.session_state.remaining_time = 0

def backToTop():
    st.session_state.movePageTo = {"directory":"contents/top.py","title":"トップ"}


def start(studyTime_p, RestTime_p):
    if not st.session_state.isTimerScene:
        st.session_state.study_time = studyTime_p
        st.session_state.rest_time = RestTime_p
        st.session_state.start_time = time.time() - st.session_state.remaining_time
        st.session_state.isTimerScene = True
        st.session_state.isTimerRunning = True
        st.rerun()


@st.dialog("確認")
def backToTop_dialog():
    st.write("トップに戻りますか?")
    st.write("トップに戻るとタイマーが終了しますが")
     
    st.button("はい", use_container_width=True, on_click=backToTop)
    st.button("いいえ", use_container_width=True)


st.button("<<トップに戻る", on_click=backToTop)
st.title("記録")


if not st.session_state.isTimerScene:
    timer_type = st.radio('タイマーの種類', ['カウントダウン','ストップウォッチ'])

    if timer_type == "カウントダウン":
        col1, col2, col3= st.columns(3)
        study_time_input = col1.number_input("学習時間(分)", min_value=0, max_value=50, step=5, value=25)
        rest_time_input = col2.number_input("休憩時間(分)", min_value=1, max_value=10, step=1, value=5)
        print("555")
        col1,col2= st.columns(2)
        confirm_button = col1.button("開始", type="primary" ,on_click=start, args=(study_time_input, rest_time_input))
    elif timer_type == "ストップウォッチ":

        with st.form("timerSettings", clear_on_submit=False):

            confirm_button = st.form_submit_button("開始", type="secondary" , use_container_width=True)

if st.session_state.isTimerScene:
    col1, col2, col3, col4, col5,= st.columns(5)
    pause_button = col1.button("一時停止")
    restart_button = col2.button("再開")
    reset_button = col3.button("リセット")

    if pause_button:
        st.session_state.pause_time = time.time()
        st.session_state.remaining_time = time.time() - st.session_state.start_time
        st.session_state.isTimerRunning = False

    if restart_button:
        st.session_state.start_time = time.time() - st.session_state.remaining_time
        st.session_state.isTimerRunning = True
    
    placeholder = st.empty()

    while st.session_state.isTimerRunning:
        elapsed_time = time.time() - st.session_state.start_time
        remaining_time_sec = int(st.session_state.study_time * 60 - elapsed_time)
        with placeholder.container():  
            st.header(f"残り時間: {remaining_time_sec // 60:02d}:{remaining_time_sec % 60:02d}")
            if st.session_state.developer_mode:
                st.write(f"経過時間(秒):{elapsed_time} // 経過率{elapsed_time / (st.session_state.study_time * 60)}")
            st.progress(elapsed_time / (st.session_state.study_time * 60))
        time.sleep(0.1)

 
