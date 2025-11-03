import streamlit as st
import streamlit_calendar as st_calendar
from io import StringIO
import json
import math
import time
from datetime import datetime

if "mainstateReloadCount" not in st.session_state:
    print("\n---Session Start---------------------------------------------\n")
    st.session_state.mainstateReloadCount = 0

if "loaded_savefile" not in st.session_state:
    st.session_state.loaded_savefile = None

st.session_state.mainstateReloadCount = st.session_state.mainstateReloadCount + 1
print(st.session_state.mainstateReloadCount)

def movePage(value):

    top_page = st.Page(
    page=value["directory"], title=value["title"], default=True
    )

    print(f"ページ移動：{st.session_state.movePageTo}")
    pg = st.navigation([top_page])
    pg.run()

def loadSaveFile(file):
    st.session_state.loaded_savefile = file

def applySaveFile(file):
    obj = json.loads(file)
    st.session_state.subjects = obj["subjects"]
    st.session_state.records = obj["records"]
    st.session_state.schedules = obj["schedules"]

# movePageToが定義されていない場合、セーブデータを読み込むか選択しtopに設定して移動
if "movePageTo" not in st.session_state and st.session_state.mainstateReloadCount == 3:
    st.session_state.movePageTo = {"directory":"contents/top.py","title":"トップ"}
    movePage(st.session_state.movePageTo)

if "developer_mode" not in st.session_state:
    st.session_state.developer_mode = False

if st.session_state.mainstateReloadCount >= 3:
    movePage(st.session_state.movePageTo)


if st.session_state.mainstateReloadCount >= 1 and st.session_state.mainstateReloadCount <= 2:
    st.title("勉強記録予定アプリ(試作)")
    st.write("初めてご利用の方は「新しく始める」を選択してください。")
    st.write("保存したデータを引き継ぐ場合は以下の「Browse files」ボタンを押して保存したデータファイルを選択してください。")

    new_button = st.button("新しく始める", type="primary" , use_container_width=True)
    uploaded_file = st.file_uploader("データを読み込んでください", type="json",key="json")

#「新しく始める」が選択された場合、空のデータを作成する
    if uploaded_file is not None:
        st.session_state.loaded_savefile == uploaded_file
        bytes_data = uploaded_file.getvalue()
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        st.session_state.loaded_savefile = stringio.read()
        applySaveFile(st.session_state.loaded_savefile)
        st.rerun()
    elif new_button:
        dt = datetime.now()
        datetime_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        obj = {"last_updated":datetime_str,"subjects":[],"records":[],"schedules":[]}
        st.session_state.loaded_savefile = json.dumps(obj)
        applySaveFile(st.session_state.loaded_savefile)
        st.rerun()