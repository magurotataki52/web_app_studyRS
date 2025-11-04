import streamlit as st
import math
import time
import pandas as pd

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

def goToRecord(time):
    st.session_state.record_Initial_value = {"time": time}
    st.session_state.movePageTo = {"directory":"contents/record.py","title":"記録/直接記録"}


def start(studyTime_p, RestTime_p , Repetition_p):
    if st.session_state.timer_scene == "setting":
        st.session_state.study_time = studyTime_p
        st.session_state.rest_time = RestTime_p
        st.session_state.start_time = time.time() - st.session_state.remaining_time
        st.session_state.timer_scene = "timer"
        st.session_state.isTimerRunning = True
        st.session_state.timer_section = 0
        st.session_state.repetition = 0
        st.session_state.repetition_num = Repetition_p
            # Studying ... 0  Rest ... 1
        st.rerun()

def endTimer():
    st.session_state.isTimerRunning = False
    st.session_state.timer_scene = "result"

    st.rerun()


@st.dialog("確認")
def backToTop_dialog():
    st.write("トップに戻りますか?")
    st.write("トップに戻るとタイマーが終了しますが")
     
    st.button("はい", use_container_width=True, on_click=backToTop)
    st.button("いいえ", use_container_width=True)


st.button("<<トップに戻る", on_click=backToTop)
st.title("記録")


if st.session_state.timer_scene == "setting":
    timer_type = st.radio('タイマーの種類', ['カウントダウン','ストップウォッチ'])

    if timer_type == "カウントダウン":
        col1, col2 = st.columns(2)
        study_time_input = col1.number_input("学習時間(秒)", min_value=0, max_value=50, step=5, value=25)
        rest_time_input = col2.number_input("休憩時間(秒)", min_value=1, max_value=10, step=5, value=5)
        col1,col2 = st.columns(2)
        repirepetition_num_input = col1.number_input("繰り返す回数", min_value=1, max_value=30, step=1, value=2)
        col1,col2 = st.columns(2)
        confirm_button = col1.button("開始", type="primary" ,on_click=start, args=(study_time_input, rest_time_input, repirepetition_num_input))
    elif timer_type == "ストップウォッチ":

        with st.form("timerSettings", clear_on_submit=False):

            confirm_button = st.form_submit_button("開始", type="secondary" , use_container_width=True)

if st.session_state.timer_scene == "timer":
    col1, col2 = st.columns(2)
    pause_button = col1.button("一時停止")
    restart_button = col2.button("再開")
    # reset_button = col3.button("リセット")

    if pause_button:
        st.session_state.pause_time = time.time()
        st.session_state.remaining_time = time.time() - st.session_state.start_time
        st.session_state.isTimerRunning = False

    if restart_button:
        st.session_state.start_time = time.time() - st.session_state.remaining_time
        st.session_state.isTimerRunning = True
    
    placeholder = st.empty()

    while st.session_state.isTimerRunning:
        elapsed_sec_time = st.session_state.repetition * (st.session_state.study_time + st.session_state.rest_time) * 1
        if st.session_state.timer_section == 0:
            timer_target = elapsed_sec_time + st.session_state.study_time * 1
        else:
            timer_target = elapsed_sec_time + st.session_state.study_time + st.session_state.rest_time * 1

        elapsed_time = time.time() - st.session_state.start_time
        remaining_time_sec = int(timer_target * 1 - elapsed_time)

        with placeholder.container():
            if st.session_state.timer_section == 0:
                st.header(f"勉強中: {remaining_time_sec // 60:02d}:{remaining_time_sec % 60:02d}")
            else:
                st.header(f"休憩中: {remaining_time_sec // 60:02d}:{remaining_time_sec % 60:02d}")
            if st.session_state.developer_mode:
                
                st.write(f"経過時間(秒):{elapsed_time} // 経過率{elapsed_time / (timer_target)}")
            
            time_progress_limited = elapsed_time / ((st.session_state.study_time + st.session_state.rest_time) * st.session_state.repetition_num)
            if time_progress_limited >= 1:
                #エラー対策
                time_progress_limited = 1

            # st.progress(time_progress_limited)
            st.write("")
            st.write(f"### 残り回数：{st.session_state.repetition_num - st.session_state.repetition}")
            

            if elapsed_time >= timer_target:
                if st.session_state.timer_section == 0:
                    st.session_state.timer_section = 1
                    if st.session_state.repetition_num - 1 == st.session_state.repetition:
                        endTimer()
                else:
                    st.session_state.repetition = st.session_state.repetition + 1
                    st.session_state.timer_section = 0

                # st.session_state.start_time = time.time() - st.session_state.remaining_time
                

        time.sleep(0.1)

if st.session_state.timer_scene == "result":
    st.header("終了！")
    
    st.write("")
    st.write(f"### 今回の合計学習時間：{st.session_state.study_time * st.session_state.repetition_num}分")

    st.write("")
    st.button("記録する", type="primary" , use_container_width=True, on_click=goToRecord, args=[st.session_state.study_time * st.session_state.repetition_num])
