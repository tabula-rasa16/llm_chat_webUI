import streamlit as st
import api
import random
import time
import uuid

CODE_SUCCESS = 200





# 流式响应模拟函数
def response_generator(response):
    # response = random.choice(
    #     [
    #         "Hello there! How can I assist you today?",
    #         "Hi, human! Is there anything I can help you with?",
    #         "Do you need help?",
    #     ]
    # )
    for word in response.split():
        yield word + " "
        time.sleep(0.1)




def chat_with_model():

    st.header("欢迎使用基于大语言模型的文档问答系统")

    # 清空对话历史记录
    with st.sidebar:
        cols = st.columns(2)
        export_btn = cols[0]
        if cols[1].button(
                "清空对话",
                use_container_width=True,
        ):
            st.session_state["messages"] = []
            unique_id = str(uuid.uuid4())
            st.session_state.conv_session_id = unique_id
            st.rerun()

    #历史消息记录的渲染
    num_count = len(st.session_state.messages)
    if num_count > 5:
        st.warning("对话轮次过多，为了获得最佳效果，您可以尝试清空对话或重置聊天")
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        # if isinstance(message, HumanMessage):
        #     with st.chat_message("user"):
        #         st.markdown(message.content)
        # elif isinstance(message, AIMessage):
        #     with st.chat_message("assistant"):
        #         st.markdown(message.content)

    # prompt = st.chat_input("请输入您的问题")
    if prompt:= st.chat_input("请输入您的问题"):
        with st.chat_message("user"):
            st.markdown(prompt)  #采用markdown可以对文本、代码等非结构化/结构化的内容进行适配渲染
        st.session_state.messages.append({"role": "user", "content": prompt}) #存储历史消息
        # st.session_state["history_message"].append(HumanMessage(content=prompt)) 
        # '''要使用 HumanMessage 类需要引入 from langchain.schema import (
        #     AIMessage,
        #     HumanMessage,
        #     SystemMessage
        # )'''
        llm_message = "oops，回答出现了问题，请稍后再试"

        # 调用大模型接口
        with st.spinner("大模型正在生成回答..."):
            response = api.chat_with_llm(query = prompt,session_id= st.session_state.conv_session_id, knowledgeDB_id= st.session_state.chat_DB_id)
        if response.get("code") == CODE_SUCCESS:
            llm_message = response.get("data")
        else:
            st.error(response.get("message"))
        # st.write(response)

        with st.chat_message("assistant"):
            # todo 用作流式输出测试
            llm_message = st.write_stream(response_generator(response = llm_message))
            # st.markdown(llm_message)
        st.session_state.messages.append({"role": "assistant", "content": llm_message})
        # st.session_state["history_message"].append(AIMessage(content=llm_message))

def sidebar_content():
    # 进行初始化数据的获取
    # 获取知识库列表
    knowledge_base_data = api.get_knowledge_bases(st.session_state.user_id)
    options_map = {}
    options = []
    isNull = False
    if knowledge_base_data.get("code") == CODE_SUCCESS:
        base_list = knowledge_base_data.get("data")
        print(base_list)
        if(len(base_list) > 0):
            options_map = {option["knowledgeDB_id"]: option for option in base_list}
            options = [(option["knowledgeDB_id"], option["knowledgeDB_name"]) for option in base_list]
        else:
            isNull = True
    

    if(isNull):
        st.sidebar.warning("您目前还没有知识库,请先创建知识库")
        # st.session_state.is_new_knowledge = True
        # selected_option = None
        # selected_option_name = ""
        # if "file_after_update" not in st.session_state:
        #     st.session_state.file_after_update = []
    else:
        # 添加下拉框选择选项
        selected_option_id, selected_option_name = st.sidebar.selectbox(
            '请选择要使用的知识库:',
            options,
            format_func=lambda option: option[1]
        )
        # 获取选中选项对应的完整对象
        selected_option = options_map.get(selected_option_id)
        st.write(selected_option)
        if selected_option is not None:
            # 刷新相关的session_state
            # refresh_session_state()

            # 判断是否切换了编辑的数据库
            # if st.session_state.knowledge_base_id != selected_option["knowledgeDB_id"]:
            #     # 更新标志位
            #     st.session_state.change_knowledge_base = True
            #     # del st.session_state.preview_files
            # else:
            #     st.session_state.change_knowledge_base = False
            #     # pass


            # 添加初始化按钮
            if st.sidebar.button("初始化/重置聊天", use_container_width=True):

                # 清空会话和聊天历史
                st.session_state.conv_session_id = None
                st.session_state.messages = []

                st.session_state.chat_DB_id = selected_option["knowledgeDB_id"]

                # unique_id = uuid.uuid4()
                # st.session_state.conv_session_id = unique_id
                
                # 调用请求,加载向量库
                with st.spinner("正在加载知识库..."):
                    response = api.load_vector_DB(st.session_state.chat_DB_id)
                if response.get("code") == CODE_SUCCESS:
                    # 创建会话session_id
                    unique_id = str(uuid.uuid4())
                    st.session_state.conv_session_id = unique_id
                else:
                    st.error(response.get("message"))




            # # 可以在这里使用selected_option对象向后端发送请求
            # option_id = selected_option["knowledgeDB_id"]
           

def main():
    # 检查用户是否登录
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        # 居中显示"请先登录"
        st.markdown(
            """
            <div style='text-align: center; margin-top: 50px;'>
                <h3>请先登录</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:

        # 如果用户已登录,渲染页面内容

        # 初始化相关的session_state

        # if "is_new_knowledge" not in st.session_state:
        #     st.session_state.is_new_knowledge = False

        # if "change_knowledge_base" not in st.session_state:
        #     st.session_state.change_knowledge_base = False

        # # 初始化文件列表
        # if "file_list" not in st.session_state:
        #     st.session_state.file_list = []


        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "cur_conv_name" not in st.session_state:
            st.session_state.cur_conv_name = []
        if "conversation_ids" not in st.session_state:
            st.session_state.conversation_ids = []
        if "cur_llm_model" not in st.session_state:
            st.session_state.cur_llm_model = []

        # 初始化当前选择的数据库Id
        if "chat_DB_id" not in st.session_state:
            st.session_state.chat_DB_id = None

        # 初始化当前对话的session Id
        if "conv_session_id" not in st.session_state:
            st.session_state.conv_session_id = None

        sidebar_content()

        if st.session_state.conv_session_id is not None:
            # 渲染对话框
            chat_with_model()
        else:
            # 渲染提示信息
            st.markdown(
            """
            <div style='text-align: center; margin-top: 50px;'>
                <h3>请先选择使用的知识库</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
    

        # chat_with_model()

if __name__ == "__main__":
    main()