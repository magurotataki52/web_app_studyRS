import streamlit as st
import uuid

sbjName_list = []
for i in range(len(st.session_state.subjects)):
    sbjName_list.append(st.session_state.subjects[i]["name"])

def back():
    if st.session_state.movedFrom == "record":
        st.session_state.movePageTo = {"directory":"contents/record.py","title":"直接記録"}
    elif st.session_state.movedFrom == "schedule":
        st.session_state.movePageTo = {"directory":"contents/schedule.py","title":"予定作成"}

@st.dialog('教科を追加する')
def addSubject_dialog():
    col1, col2 = st.columns(2)
    name = col1.text_input('名前')
    color = col2.color_picker('色', "#6d6d6d")
    if st.button('追加', type="primary" , use_container_width=True):
        if name in sbjName_list:
            st.warning("重複する教科名は使用できません")
        else:
            st.session_state.addSubject = {'name': name,"color": color}
            st.rerun()

@st.dialog('教科を編集')
def editSubject_dialog(target):
    col1, col2 = st.columns(2)
    name = col1.text_input('名前', value=st.session_state.subjects[target]["name"], disabled=True)
    color = col2.color_picker('色',value=st.session_state.subjects[target]["color"])
    if col1.button('決定', type="primary" , use_container_width=True):
        st.session_state.editSubject = {'mode': 'edit','target': target,'name': name,"color": color}
        st.rerun()
    if col2.button('削除', use_container_width=True):
        st.session_state.editSubject = {'mode': 'delete','target': target,'name': name,"color": color}
        st.rerun()

if "addSubject" not in st.session_state:
    st.session_state.addSubject = ""

if "editSubject" not in st.session_state:
    st.session_state.editSubject = ""

if not st.session_state.addSubject == "":
    st.session_state.subjects.append({"name":st.session_state.addSubject["name"],"color":st.session_state.addSubject["color"]})
    st.session_state.addSubject = ""

if not st.session_state.editSubject == "":
    if st.session_state.editSubject["mode"] == "edit":
        del st.session_state.subjects[st.session_state.editSubject["target"]]
        st.session_state.subjects.insert(st.session_state.editSubject["target"], {"name":st.session_state.editSubject["name"],"color":st.session_state.editSubject["color"]})
    elif st.session_state.editSubject["mode"] == "delete":
        del st.session_state.subjects[st.session_state.editSubject["target"]]
    st.session_state.editSubject = ""

st.button("<<戻る", on_click=back) 

st.header("教科設定")

st.button("教科を追加する", on_click=addSubject_dialog)
st.write("")
st.write("## 教科リスト")
for i in range(len(st.session_state.subjects)):
    col1,col2,col3= st.columns(3)
    col1.write(f"#### □ {st.session_state.subjects[i]["name"]}")
    col2.color_picker('色', st.session_state.subjects[i]["color"], key=uuid.uuid4(), disabled=True, label_visibility="hidden")
    col3.button("編集", key=uuid.uuid4(), on_click=editSubject_dialog, args=[i])