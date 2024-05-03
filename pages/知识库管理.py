import streamlit as st
import pandas as pd
import api
import io
import base64
import time

CODE_SUCCESS = 200

def render_knowledge_base_page():

    # 设置页面标题
    st.set_page_config(page_title="kn")


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
    options.append((-1, "➕创建新知识库"))
    options_map[-1] = {"knowledgeDB_id": -1, "knowledgeDB_name": "➕创建新知识库"}



    if(isNull):
        st.sidebar.warning("您目前还没有知识库,请先创建知识库")
        st.session_state.is_new_knowledge = True
        selected_option = None
        selected_option_name = ""
        if "file_after_update" not in st.session_state:
            st.session_state.file_after_update = []
    else:
        # 添加下拉框选择选项
        selected_option_id, selected_option_name = st.sidebar.selectbox(
            '请选择要操作的知识库:',
            options,
            format_func=lambda option: option[1]
        )
        # 获取选中选项对应的完整对象
        selected_option = options_map.get(selected_option_id)
        st.write(selected_option)
        if selected_option is not None and selected_option["knowledgeDB_id"] != -1:
            # 刷新相关的session_state
            refresh_session_state()

            # 判断是否切换了编辑的数据库
            if st.session_state.knowledge_base_id != selected_option["knowledgeDB_id"]:
                # 更新标志位
                st.session_state.change_knowledge_base = True
                # del st.session_state.preview_files
            else:
                st.session_state.change_knowledge_base = False
                # pass

            st.session_state.knowledge_base_id = selected_option["knowledgeDB_id"]

            # 可以在这里使用selected_option对象向后端发送请求
            option_id = selected_option["knowledgeDB_id"]
            # 调用后端接口,获取知识库中包含的文件列表
            st.write(option_id)
            current_files_list_response = api.get_files_in_knowledge_base(option_id)
            if current_files_list_response.get("code") == CODE_SUCCESS:
                current_files_list = current_files_list_response.get("data")

                # 将获取的数据持久化储存
                if "file_after_update" not in st.session_state or st.session_state.change_knowledge_base:
                    st.session_state.file_after_update = current_files_list[:]
                    st.write(st.session_state.file_after_update)

                # st.write(current_files_list)
                # 提取current_files_list中每个元素的document_name值,存储在一个新列表中
                file_names = [item["document_name"] for item in current_files_list]
                create_times = [item["create_time"] for item in current_files_list]

                true_emoji = "✅"
                false_emoji = "❌"

                in_vectorDBs = [true_emoji if item["in_vectorDB"] == "1" else false_emoji for item in current_files_list]

                file_num = len(file_names)



                # 将新列表作为st.session_state.process_data["文件名称"]的值
                st.session_state.process_data["文件名称"] = file_names[:] #需要进行浅拷贝
                st.session_state.process_data["文档入库时间"] = create_times
                st.session_state.process_data["源文件"] = [true_emoji] * file_num
                st.session_state.process_data["向量库"] = in_vectorDBs

                # 将库中原有的文件列表存储在st.session_state.file_list中
                st.session_state.file_list = file_names[:]
                # st.session_state.file_list = current_files_list

            else:
                st.error("获取文件列表失败: " + current_files_list_response.get("message"))

        elif selected_option["knowledgeDB_id"] == -1 and st.session_state.knowledge_base_id != selected_option["knowledgeDB_id"]:
            # 为新建知识库
            refresh_session_state()

            st.session_state.is_new_knowledge = True

            st.session_state.preview_files = []

            st.session_state.file_after_update = []

            st.session_state.change_knowledge_base = True

            st.session_state.knowledge_base_id = selected_option["knowledgeDB_id"]
            # st.session_state.preview_files = []



    # create_knowledgeDB = st.sidebar.button("创建新知识库")
    # if create_knowledgeDB:
    #     st.session_state.is_new_knowledge = True





    # 如果 session_state 中没有 preview_files 键,则初始化它
    if "preview_files" not in st.session_state or st.session_state.change_knowledge_base:
        st.session_state.preview_files = st.session_state.file_list[:]
        # st.session_state.preview_files = st.session_state.process_data[:]
        # st.session_state.preview_files_rows = {filename: False for filename in st.session_state.preview_files}


    # 知识库名称
    current_db_name = selected_option_name if selected_option is not None else ""
    st.subheader("知识库信息配置")
    after_update_db_name = st.text_input("在此修改知识库名称:", value = current_db_name, key="knowledge_base_name")





    # 创建文件上传区域
    st.subheader("上传相关文件:")
    uploaded_file = st.file_uploader("在此选择文件或拖拽文件至此", accept_multiple_files=False)
    # st.write(uploaded_file)

    if uploaded_file is not None:
        # 读取文件内容
        file_bytes = uploaded_file.getvalue()

        # 对文件字节流进行 base64 编码
        file_bytes_base64 = base64.b64encode(file_bytes).decode('utf-8')

        file_name = uploaded_file.name
        # 将字节流转换为文件对象
        # st.write(type(file_obj))
        if st.button("上传"):
            response = api.upload_file(file_name=file_name, file_bytes=file_bytes_base64)
            st.write(response)
            if response.get("code") == CODE_SUCCESS:
                file_name_after = response.get("data")["file_name"]
                if file_name_after != None:

                    new_file = {
                        "document_name": file_name_after,
                        "del_flag": "0",
                        "in_vectorDB": "1"
                    }
                    st.session_state.file_after_update.append(new_file)

                    st.session_state.file_list.append(file_name_after)
                    st.session_state.preview_files.append(file_name_after)


                    # st.session_state.preview_files_rows[file_name_after] = False
                st.success("文件上传成功!")
                # st.write(st.session_state.file_list)
                # st.write(st.session_state.process_data)
            else:
                st.error("文件上传失败: " + response.get("message"))

    # 创建文本输入框
    st.subheader("文件处理配置")
    max_source_length = st.number_input("单行文本最大长度:", min_value=1, value=250)
    max_target_length = st.number_input("目标文本最大长度:", min_value=1, value=50)
    # remove_blank_lines = st.checkbox("去除中文标题前空")

    # 使用HTML标签渲染分割线
    st.markdown("""---""")
    # st.markdown("""
    # <hr style="height:2px;border-width:0;color:gray;background-color:gray">
    # """, unsafe_allow_html=True)

    # 显示上传的文件列表
    st.subheader("知识库中现有文件:")
    if st.session_state.process_data["文件名称"] is not None:
        # file_list = [f.name for f in uploaded_files]
        # st.table({"文件名": file_list})
        process_data_table = st.table(st.session_state.process_data)
    else:
        st.write("知识库中目前还没有文件,请先上传文件后再操作")



    # 显示变更后知识库的文件列表预览
    # preview_files = st.session_state.file_list

    # # 如果 session_state 中没有 preview_files 键,则初始化它
    # if "preview_files" not in st.session_state:
    #     st.session_state.preview_files = st.session_state.file_list[:]
    #     st.write(st.session_state.preview_files)
    #     st.session_state.preview_files_rows = {filename: False for filename in st.session_state.preview_files}
    #     st.write(st.session_state.preview_files_rows)

    if len(st.session_state.preview_files) > 0:
        st.subheader("变更区库内文件预览:")

        # 创建一个DataFrame来存储文件名和选择状态
        data = pd.DataFrame({'文件名': st.session_state.preview_files,
                            '选择': [False] * len(st.session_state.preview_files),
                            # '源文件': st.session_state.process_data["源文件"],
                            # '向量库': st.session_state.process_data["向量库"]
                            })

        # 显示可编辑表格
        edited_data = st.data_editor(
            data,
            column_config={
                '选择': st.column_config.CheckboxColumn(
                    "选择",
                    help="选择或取消选择该文件",
                    width="small",
                )
            },
            disabled=["文件名","源文件","向量库"],
            hide_index=True,
        )

        # 获取选中的文件名
        selected_files = edited_data[edited_data['选择']]['文件名'].tolist()
        st.write(f"Selected files: {', '.join(selected_files)}")

        # preview_files_rows = [st.checkbox(row, key=f"row_{i}") for i, row in enumerate(preview_files)]

        # # 添加按钮
        # selected_any = any(preview_files_rows)
        # st.write(preview_files)

        # st.subheader("变更区库内文件预览:")
        # preview_files_rows = {filename: st.checkbox(filename, key=filename) for filename in preview_files}

        # # 添加按钮
        # # selected_any = any(preview_files_rows)
        # # st.write(preview_files)
        # selected_files = [filename for filename, checked in preview_files_rows.items() if checked]
        # st.write(f"Selected files: {', '.join(selected_files)}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button("下载所选文件", disabled=not selected_files)
        with col2:
            add_to_vectorDB = st.button("添加至向量库", disabled=not selected_files)
            if add_to_vectorDB:
                for file_info in st.session_state.file_after_update:
                    # 检查文件名是否在selected_files列表中
                    if file_info["document_name"] in selected_files:
                        # 如果在,将in_vectorDB字段置为"1"
                        file_info["in_vectorDB"] = "1"
                st.write(st.session_state.file_after_update)
        with col3:
            remove_from_vectorDB = st.button("从向量库中移出", disabled=not selected_files)
            if remove_from_vectorDB:
                for file_info in st.session_state.file_after_update:
                    # 检查文件名是否在selected_files列表中
                    if file_info["document_name"] in selected_files:
                        # 如果在,将in_vectorDB字段置为"0"
                        file_info["in_vectorDB"] = "0"
                st.write(st.session_state.file_after_update)

        with col4:
            delete_from_knowledgeDB = st.button("从知识库中删除", disabled=not selected_files)
            if delete_from_knowledgeDB:
                # todo 可引入streamlit_modal实现弹出框效果
                for file_info in st.session_state.file_after_update:
                    # 检查文件名是否在selected_files列表中
                    if file_info["document_name"] in selected_files:
                        # 如果在,将del_flag字段置为"1"
                        file_info["del_flag"] = "1"
                st.write(st.session_state.file_after_update)
                # if st.button("撤销删除操作"):
                #     st.write("已撤销删除操作")
                #     for file_info in st.session_state.file_after_update:
                #         # 检查文件名是否在selected_files列表中
                #         if file_info["document_name"] in selected_files:
                #             # 如果在,将del_flag字段置为"0"
                #             file_info["del_flag"] = "0"
                #     st.write(st.session_state.file_after_update)

    else:
        pass
        # st.write("知识库中目前还没有文件,请先上传文件后再操作")



    # 在需要渲染分割线的位置添加以下代码
    st.markdown("""---""")

    # 添加底部按钮
    container = st.container()  # 创建一个容器
    col1, col2, col3 = container.columns([2, 3, 1])  # 将容器分为三列,中间列占据大部分宽度

    # 将两个按钮放在中间列中
    # with col2:
    #     left_col, right_col = st.columns(2)
    #     with left_col:
    #         st.button("保留选文本重新向量化")
    #     with right_col:
    #         st.button("删除知识库")
    # 将两个按钮放在左右两侧
    with col1:
        commit_change = st.button("依据源文件新建/重新加载知识库")
        if commit_change:
            # 判断为新建知识库还是更新知识库
            if st.session_state.is_new_knowledge:
                st.write("************")
                # 为新建知识库

                # # 使用st.cache_resource调用异步函数
                # create_refresh_task = st.cache_resource.get_async("create_and_refresh", create_and_refresh, st.session_state.user_id, after_update_db_name, after_update_db_name, st.session_state.file_after_update)

                # # 使用st.cache_data缓存响应结果
                # with st.spinner("正在处理请求..."):
                #     update_response, refresh_response = st.cache_data.get(create_refresh_task.uuid)


                # # 处理响应结果
                # if update_response and update_response.get("code") == CODE_SUCCESS:
                #     st.success("知识库新建成功!")
                #     if refresh_response and refresh_response.get("code") == CODE_SUCCESS:
                #         st.success("向量库刷新成功!")
                #     else:
                #         st.error("向量库刷新失败!")
                # else:
                #     st.error("知识库新建失败!")

                with st.spinner("正在新建知识库..."):
                    response = api.create_knowledge_base(st.session_state.user_id, after_update_db_name, after_update_db_name, st.session_state.file_after_update)

                if response.get("code") == CODE_SUCCESS:
                    st.success("知识库新建成功!")

                    knowledgeDB_id = response.get("data").get("knowledgeDB_id")

                    # st.write(knowledgeDB_id)

                    # 发送刷新向量库请求
                    with st.spinner("正在刷新向量库..."):
                        refresh_response = api.refresh_vector_DB(knowledgeDB_id)

                    if refresh_response and refresh_response.get("code") == CODE_SUCCESS:
                        st.success("向量库刷新成功!")

                        # 刷新session_state
                        delete_session_state()
                        st.experimental_rerun()
                    else:
                        st.error("向量库刷新失败:" + refresh_response.get("message"))
                else:
                    st.error("知识库创建失败:" + response.get("message"))

            else:
                # 为更新知识库

                # # 使用st.cache_resource调用异步函数
                # update_refresh_task = st.cache_resource.get_async("update_and_refresh", update_and_refresh, st.session_state.knowledge_base_id, after_update_db_name, st.session_state.file_after_update)

                # # 使用st.cache_data缓存响应结果
                # with st.spinner("正在处理请求..."):
                #     update_response, refresh_response = st.cache_data.get(update_refresh_task.uuid)


                # # 处理响应结果
                # if update_response and update_response.get("code") == CODE_SUCCESS:
                #     st.success("知识库更新成功!")
                #     if refresh_response and refresh_response.get("code") == CODE_SUCCESS:
                #         st.success("向量库刷新成功!")
                #     else:
                #         st.error("向量库刷新失败!")
                # else:
                #     st.error("知识库更新失败!")


                with st.spinner("正在更新知识库..."):
                    response = api.update_knowledge_base(st.session_state.knowledge_base_id, after_update_db_name, st.session_state.file_after_update)

                if response.get("code") == CODE_SUCCESS:
                    st.success("知识库更新成功!")

                    # 发送刷新向量库请求
                    with st.spinner("正在刷新向量库..."):
                        refresh_response = api.refresh_vector_DB(st.session_state.knowledge_base_id)

                    if refresh_response and refresh_response.get("code") == CODE_SUCCESS:
                        st.success("向量库刷新成功!")

                        # 刷新session_state
                        delete_session_state()
                        st.experimental_rerun()
                    else:
                        st.error("向量库刷新失败:" + refresh_response.get("message"))
                else:
                    st.error("知识库更新失败:" + response.get("message"))


                # response = api.update_knowledge_base(st.session_state.knowledge_base_id, after_update_db_name, st.session_state.file_after_update)
                # if response.get("code") == CODE_SUCCESS:
                #     with st.spinner("正在更新知识库..."):
                #         time.sleep(2)
                #     st.write("知识库更新成功")
                #     time.sleep(2)
                #     delete_session_state()
                #     st.experimental_rerun()
                # else:
                #     st.write("知识库更新失败:", response.get("message"))

    with col3:
            delete_knowledgeDB = st.button("删除知识库")
            if delete_knowledgeDB:
                # todo 可引入streamlit_modal实现弹出框效果
                response = api.delete_knowledge_base(st.session_state.knowledge_base_id)
                if response.get("code") == CODE_SUCCESS:
                    with st.spinner("正在删除知识库..."):
                        time.sleep(2)
                    st.write("知识库删除成功")
                    time.sleep(2)
                    delete_session_state()
                    st.experimental_rerun()
                else:
                    st.write("知识库删除失败:", response.get("message"))

# 获取知识库数据
# def get_knowledge_base_data():
#     response = api.get_knowledge_bases(st.session_state.user_id)

#     return knowledge_base_data


# 异步创建知识库
async def create_and_refresh(user_id, knowledgeDB_name, discription, file_list):
    # 发送更新知识库请求
    with st.spinner("正在新建知识库..."):
        update_response = api.create_knowledge_base(user_id, knowledgeDB_name, discription, file_list)

    # 检查更新知识库请求是否成功
    if update_response.get("code") == 200:
        knowledgeDB_id = update_response.get("data").get("knowledge_base_id")
        # 发送刷新向量库请求
        with st.spinner("正在刷新向量库..."):
            refresh_response = api.refresh_vector_DB(knowledgeDB_id)

        # 返回两个请求的响应
        return update_response, refresh_response
    else:
        # 如果更新知识库请求失败,则只返回更新请求的响应
        return update_response, None


# 异步更新知识库
async def update_and_refresh(knowledgeDB_id, knowledgeDB_name, file_list):
    # 发送更新知识库请求
    with st.spinner("正在更新知识库..."):
        update_response = api.update_knowledge_base(knowledgeDB_id, knowledgeDB_name, file_list)

    # 检查更新知识库请求是否成功
    if update_response.get("code") == 200:
        # 发送刷新向量库请求
        with st.spinner("正在刷新向量库..."):
            refresh_response = api.refresh_vector_DB(knowledgeDB_id)

        # 返回两个请求的响应
        return update_response, refresh_response
    else:
        # 如果更新知识库请求失败,则只返回更新请求的响应
        return update_response, None

# 刷新相关的session_state
def refresh_session_state():
    st.session_state.file_list = []
    st.session_state.process_data = {
            "文件名称": None,
            "文档入库时间": None,
            "源文件": None,
            "向量库": None
        }
    st.session_state.is_new_knowledge = False
    st.session_state.change_knowledge_base = False
    # st.session_state.file_after_update = []
    # st.session_state.preview_files = []
    # st.session_state.preview_files_rows = []

# 删除相应的session_state
def delete_session_state():
    del st.session_state.file_list
    del st.session_state.process_data
    del st.session_state.file_after_update
    del st.session_state.preview_files
    # del st.session_state.preview_files_rows

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

        if "is_new_knowledge" not in st.session_state:
            st.session_state.is_new_knowledge = False

        if "change_knowledge_base" not in st.session_state:
            st.session_state.change_knowledge_base = False

        # 初始化文件列表
        if "file_list" not in st.session_state:
            st.session_state.file_list = []

        # 初始化当前选择的数据库Id
        if "knowledge_base_id" not in st.session_state:
            st.session_state.knowledge_base_id = None

        # 初始化知识库内文件表格对象
        if "process_data" not in st.session_state:
            st.session_state.process_data = {
                "文件名称": None,
                "文档入库时间": None,
                "源文件": None,
                "向量库": None
            }

        # # 初始化知识库内文件修改后结果对象
        # if "file_after_update" not in st.session_state:
        #     st.session_state.file_after_update = []


        render_knowledge_base_page()

if __name__ == "__main__":
    main()
