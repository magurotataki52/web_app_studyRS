import streamlit as st


def backToTop():
    st.session_state.movePageTo = {"directory":"contents/top.py","title":"トップ"}


st.button("<<トップに戻る", on_click=backToTop)   
st.header("準備中")