import streamlit as st
import api
import time

CODE_SUCCESS = 200


def render_login_page():
    st.title("用户登录")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")

    login_error = ""

    if st.button("登录"):
        # 进行填写完整性校验
        if not username or not password:
            login_error = "请输入用户名和密码"
        else:
            # st.write("登录成功")
            response = api.login_user(username, password)
            if response.get("code") == CODE_SUCCESS:
                # 获取当前登录用户id并存储
                st.session_state.user_id = response.get("data").get("user_id")
                st.success("登录成功!")
            else:
                login_error = response.get("message")
    
    if login_error:
        st.error(login_error)
    
    register_clicked = st.button("还没有账号？点此注册")
    if register_clicked:
        st.session_state.page = "register"
        st.experimental_rerun()

def render_register_page():
    st.title("用户注册")
    username = st.text_input("用户名")
    # email = st.text_input("邮箱")
    password = st.text_input("密码", type="password")

    login_error = ""

    if st.button("注册"):
        # 进行填写完整性校验
        if not username or not password:
            login_error = "请输入用户名和密码"
        else:
            # st.write("注册成功")
            response = api.register_user(username, password)
            # st.write(response)
            if response.get("code") == CODE_SUCCESS:
                st.success("注册成功! 正在返回登录页...")
                st.session_state.page = "login"
                time.sleep(1)
                st.experimental_rerun()
            else:
                login_error = response.get("message")
    
    if login_error:
        st.error(login_error)

    login_clicked = st.button("已有账号？点此登录")
    if login_clicked:
        st.session_state.page = "login"
        st.experimental_rerun()

def main():
    # st.set_page_config(page_title="User Authentication")

    st.set_page_config(page_title="基于文档的问答系统", page_icon=":robot:", layout="wide")

    st.title("基于文档的问答系统")

    if "page" not in st.session_state:
        st.session_state.page = "login"
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if st.session_state.page == "login":
        render_login_page()
    elif st.session_state.page == "register":
        render_register_page()

if __name__ == "__main__":
    main()