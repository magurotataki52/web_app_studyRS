import streamlit as st
import streamlit_calendar as st_calendar
import json
import math
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

dt_now = datetime.now()

st.session_state.timer_scene = "setting"
st.session_state.isTimerRunning = False

sbjName_list = []
for i in range(len(st.session_state.subjects)):
    sbjName_list.append(st.session_state.subjects[i]["name"])

sbjColor_list = []
for i in range(len(st.session_state.subjects)):
    sbjName_list.append(st.session_state.subjects[i]["color"])

if st.session_state.loaded_savefile is not None:
    parsed_data = json.loads(str(st.session_state.loaded_savefile))
else:
    parsed_data = None

def goToTimer():
    st.session_state.movePageTo = {"directory":"contents/timer.py","title":"記録/タイマー"}

def goToRecord():
    st.session_state.record_Initial_value = {"time": 0}
    st.session_state.movePageTo = {"directory":"contents/record.py","title":"記録/直接記録"}


# Header

st.title("勉強記録予定アプリ(試作)")

if st.session_state.loaded_savefile is not None:
    st.write(f"最終更新：{parsed_data['last_updated']}")
st.write("")

#データ保存 --------------------------------------------------
dt = datetime.now()
datetime_str = dt.strftime("%Y-%m-%d %H:%M:%S")
last_updated = datetime_str
subjects = st.session_state.subjects
records = st.session_state.records
schedules = st.session_state.schedules

obj = {
    "last_updated": last_updated,
    "subjects": subjects,
    "records": records,
    "schedules": schedules
}

json_txt = json.dumps(obj, default=str)
print(json_txt)

st.download_button("データを保存する", type="primary", data=json_txt, file_name="studyRS_savedata.json",mime="text/json")

#------------------------------------------------------------

st.write("## イベント")
st.write("「期末考査」まであと")
st.write("### 25日")

st.write("")

st.write("## 記録")
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

#-カレンダー-------------------------------------------------------------------------

#event1 = {
#    'id': '1', # イベントを識別するためのID。重複不可
#    'title': '単語帳15p', # イベント名
#    'start': '2025-11-10T00:00:00',
#    'allDay': 'true',
#}

# calendarにはイベント一覧を配列にして渡す
event_list = []
eventId = 0
for schedule in st.session_state.schedules:
        eventId = eventId + 1
        print(f"予定読み込み | 日時:{schedule["date"]} タイトル:{schedule["title"]} 教科:{schedule["subject"]} 時間:{schedule["time"]} ID:{eventId}")

        #設定されている教科がリストにあるか？
        if schedule["subject"] in sbjName_list:
            color = st.session_state.subjects[sbjName_list.index(schedule["subject"])]["color"]
        else:
            color = "#888888"

        event_list.append({
                "id": eventId,
                "title": schedule["title"],
                "start": f"{schedule["date"]}T00:00:00",
                "allDay": "true",
                "color": color
            }
        )

print(event_list)
options = {
    'initialView': 'dayGridMonth',
    'headerToolbar': {
        # ヘッダーの左側に表示するものを指定
        # 日付を移動するボタンが表示される。'today'を省略してもいい
        'left': 'today prev,next',
        # ヘッダーの中央に表示するものを指定
        # 'title'は表示されている日付などのこと
        'center': 'title',
        # ヘッダーの右側に表示するものを指定
        # ビュー名をカンマ区切りで列挙して指定するとビューを切り替えるためのボタンが表示される
        'right': 'dayGridMonth,listWeek',
    },
    'buttonText': {
        'today': '今日',
        'month': 'カレンダー',
        'list': 'リスト',
        'all-day': '終日'
        },
    'locale': 'ja', # 日本語化する
}

# イベントを表示するカレンダーを作成
st_calendar.calendar(events=event_list,options=options)

st.write("")
st.write("")
st.write("### 学習記録")
#----------------------------------------------------------------------------------------
#6日前から今日までの記録を探す
for i in range(7):
    dt = datetime.now()
    search_date = dt + timedelta(days=-6+i)
    datetime_str = search_date.strftime("%Y-%m-%d")
    print(datetime_str)


chart_data = pd.DataFrame(
   {"曜日": ["日","月","火","水","木","金","土"], "国語": [5,0,25,40,5,0,25], "数学": [60,0,30,30,25,50,0], "英語": [0,50,25,40,30,25,25]}
)

st.bar_chart(
   chart_data, x="曜日", y=["国語","数学","英語"], color=["#EB6666","#4694DD","#D443CD"],  y_label="学習時間(分)"# Optional
)