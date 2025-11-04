import streamlit as st

def backToTop():
    st.session_state.movePageTo = {"directory":"contents/top.py","title":"トップ"}

st.success("✓ 記録が完了しました。")

st.button("トップに戻る",use_container_width=True,type="primary",on_click=backToTop())
st.button("記録画面に戻る",use_container_width=True,type="secondary",on_click=backToTop())
