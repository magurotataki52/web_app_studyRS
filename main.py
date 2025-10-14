import streamlit as st
import streamlit_calendar as st_calendar
import math
import time
import datetime

if "isFirstRun" not in st.session_state:
    st.session_state.isFirstRun = True
else:
    st.session_state.isFirstRun = False

def movePage(value):

    top_page = st.Page(
        page=value["directory"], title=value["title"], default=True
    )

    print(f"ページ移動：{st.session_state.movePageTo}")
    pg = st.navigation([top_page])
    pg.run()


# movePageToが定義されていない場合、topに設定して移動
if "movePageTo" not in st.session_state:
    st.session_state.movePageTo = {"directory":"contents/top.py","title":"トップ"}
    movePage(st.session_state.movePageTo)

if "developer_mode" not in st.session_state:
    st.session_state.developer_mode = False

if not st.session_state.isFirstRun:
    movePage(st.session_state.movePageTo)


