import streamlit as st
import streamlit_calendar as st_calendar
import math
import time
import datetime

dt_now = datetime.datetime.now()

st.session_state.timer_scene = "setting"
st.session_state.isTimerRunning = False

def goToTimer():
    st.session_state.movePageTo = {"directory":"contents/timer.py","title":"記録/タイマー"}
def goToRecord():
    st.session_state.movePageTo = {"directory":"contents/record.py","title":"記録/直接記録"}

# Header
st.title("勉強記録予定アプリ(試作)")

st.write("")
st.write("")

st.write("## 記録")
st.write(dt_now.strftime('%Y年%m月%d日 %H:%M:%S'))
st.button("タイマーで記録する", type="primary" , use_container_width=True, on_click=goToTimer)
st.button("直接記録する", type="primary" , use_container_width=True, on_click=goToRecord)

st.write("")
st.write("")

st.write("### Todo")
st.write("##### ・項目１")
st.write("##### ・項目２")
st.write("##### ・項目３")

st.write("")
st.write("")

st_calendar.calendar()
if st.session_state.developer_mode:
    devmode = 1
else:   
    devmode = 0
st.session_state.developer_mode = st.radio("開発者モード", options=[False,True], index=devmode)