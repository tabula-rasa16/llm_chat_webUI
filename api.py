import requests

# API_BASE_URL = "http://localhost:8000" #后端地址

API_BASE_URL = "https://dsw-gateway-cn-shanghai.data.aliyun.com/dsw-335899/proxy/8000" #阿里云地址



HEADERS = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
  'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
  'cache-control': 'max-age=0',
  'cookie': 'username-dsw-gateway-cn-shanghai-data-aliyun-com=2|1:0|10:1711259647|48:username-dsw-gateway-cn-shanghai-data-aliyun-com|196:eyJ1c2VybmFtZSI6ICJkYzUyZjU5MjM3NzI0NDhhOTdlMGEyNzM1OGU3ZTE4OCIsICJuYW1lIjogIkFub255bW91cyBIaW1hbGlhIiwgImRpc3BsYXlfbmFtZSI6ICJBbm9ueW1vdXMgSGltYWxpYSIsICJpbml0aWFscyI6ICJBSCIsICJjb2xvciI6IG51bGx9|be1b352345e8ee524e9d3a0f04e569418038f12f05d4a38d4ec36fa4dc8baca8; _xsrf=2|ae31cb38|d64cfefc482ccdd85a3be04f1a318bb5|1712846107; cna=Hah1HpcTPUoCAW+7fArQ2gPR; bs_n_lang=zh_CN; _bl_uid=hRlUptCRmepsbql6k8086dsmCkbn; _samesite_flag_=true; cookie2=123ff429140a21d34e7c255bed8e113f; aliyun_lang=zh; bd=s0ouCmI%3D; help_csrf=IFEJmg0jiOe99hw9Yy41UdggyeB8a%2BESaajbghqjsRsX%2BwMct5iExsOcIiQOFBUNosU8opwLFGvnc2o40mkm9OYq%2BHPXmi8JCSm1uSwPbDUymEdljZqOPlvpE0Sle7RIX1t3Peq%2BbwMe76bemq4spg%3D%3D; cr_token=b1f65097-abd6-470e-a5dc-8678dea1b263; _tb_token_=71363035b3773; cnaui=2052****sunze; aui=2052****sunze; ecsCustomBuyVersion=new; _ali_s_gray_t=54; _ali_s_gray_v=onesite,au,in,vn; activeRegionId=cn-shanghai; channel=CRjieg55GXaeceFQpoEUt%2Fr341TiTP1QALA7ykJNfsFQODFTrkLdO59OPiQMX0b2XRx%2Bh05Z784%2BBbJBQmxWWA%3D%3D; currentRegionId=cn-shanghai; munb=2213952980533; csg=c9d822fb; t=79f77fbad8c46f7204c096307354a24a; login_aliyunid_ticket=fKJzxdnb95hYssNIZor6q7SCxRtgmGCbifG2Cd4ZWazmBdHI6sgXZqg4XFWQfyKpeu*0vCmV8s*MT5tJl3_1$$wqhfGKH1uCZpWKPDbhPcVk6z2C*MXNj7Ui379P1T3Mwf_ENpoU_BOTwChTBoNM1Zee0; login_aliyunid_csrf=_csrf_tk_1285113335184840; login_aliyunid_pk=1533249480222381; login_current_pk=1533249480222381; hssid=CN-SPLIT-ARCEByIOc2Vzc2lvbl90aWNrZXQyAQE47Njw1e4xQAFKEEiDQSjuU38PnWqi2dfdL1E7Ukl56HCk4MQnoawTI7KAhIiOGA; hsite=6; aliyun_country=CN; aliyun_site=CN; login_aliyunid=2052****sunze; c_token=56fa079e8dc558f57a1d49e40b29b4b5; ck2=53b12c269be25948cbe54d537d37035d; an=2052635sunze; lg=true; sg=e11; aliyun_cert_type_common=1; FECS-XSRF-TOKEN=jqUVFSb4; yunpk=1533249480222381; cna=Hah1HpcTPUoCAW+7fArQ2gPR; sca=ecbb1855; atpsida=61e90f264da482f1eb488c33_1713338832_4; tfstk=f7RteymIVDmgYckD1FMH3c3p_xuHLIEw7a-_iSfcjvtdA3NgjFiwHBLXfVWDsIfxMMKS7SDwls3vjFeGnEiwDIIBxGVm7x-vDhsHmSYMMpPvzERi7s0N_F5VG0moZsLw7sowebfjrkZCre__5iD_UrfVG0m3KS6Zws-oXxvSHegdoZE_fn__O2QAli1fftZQdasCcs1XcMGCoZ2bcR6bRMGj9qjQ3iNvT0lynFDQFnK29NBIKFsCUtgcAOIW5MnxDBFdBgT1vSi-J_wfDMRSxvLexdtG8nh-v6TWp1_9cbwlApLB_Tf-FRKW-hRR1QnTswXAXpO1prNXR6SGdKKtXRS6IHBPR9axawxlAFR6pqrB53jO1w6nN4LChpANUCmQ6_9yS1vXAXF9VgkDZQK-RujRoRgKJ-yVCwArpNjcmMDbJwIoWx2439D5Jg0KJ-yVCw7dqVH03-WnF; isg=BMfEZrOEbUGbauo8M_kTbEn0VnuRzJuujxuYOpm3w9YmCOHKoZnn_zGArshW5XMm; username-dsw-gateway-cn-shanghai-data-aliyun-com="2|1:0|10:1714556349|48:username-dsw-gateway-cn-shanghai-data-aliyun-com|200:eyJ1c2VybmFtZSI6ICI3ZDQzYTJhNWJkZGM0YjZmOGNlZmYwODhkNjg0YTg4ZCIsICJuYW1lIjogIkFub255bW91cyBUaGVtaXN0byIsICJkaXNwbGF5X25hbWUiOiAiQW5vbnltb3VzIFRoZW1pc3RvIiwgImluaXRpYWxzIjogIkFUIiwgImNvbG9yIjogbnVsbH0=|edae490771aa4470d70abf71772a2de10c06f75f740fed77748f4eb1e271c0f8"',
  'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
  'Content-Type': 'application/json'
}

# 用户注册
def register_user(username, password):
    url = f"{API_BASE_URL}/user/signup"
    data = {
        "user_name": username,
        "password": password
    }
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# 用户登录
def login_user(username, password):
    url = f"{API_BASE_URL}/user/login"
    data = {
        "user_name": username,
        "password": password
    }
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# 根据用户id获取其下知识库列表
def get_knowledge_bases(user_id):
    url = f"{API_BASE_URL}/knowledgeDB/list"
    data = {
        "user_id": user_id
    }
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# 用户上传文件
def upload_file(file_name, file_bytes):
    url = f"{API_BASE_URL}/fileHandler/uploadFile"
    data = {"file_name": file_name,
            "file_bytes": file_bytes}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# 根据知识库id获取其包含的文件列表
def get_files_in_knowledge_base(knowledge_base_id):
    url = f"{API_BASE_URL}/knowledgeDB/document/list"
    data = {"knowledgeDB_id": knowledge_base_id}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# 新建知识库
def create_knowledge_base(user_id, knowledgeDB_name, discription, file_list):
    url = f"{API_BASE_URL}/knowledgeDB/create"
    data = {"user_id": user_id,
            "knowledgeDB_name": knowledgeDB_name,
            "discription": discription,
            "file_list": file_list}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# 更新知识库
def update_knowledge_base(knowledgeDB_id, knowledgeDB_name, file_list):
    url = f"{API_BASE_URL}/knowledgeDB/update"
    data = {"knowledgeDB_id": knowledgeDB_id,
            "knowledgeDB_name": knowledgeDB_name,
            "file_list": file_list}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# 删除知识库
def delete_knowledge_base(knowledgeDB_id):
    url = f"{API_BASE_URL}/knowledgeDB/delete"
    data = {"knowledgeDB_id": knowledgeDB_id}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# 刷新向量库
def refresh_vector_DB(knowledgeDB_id):
    url = f"{API_BASE_URL}/vector_DB/refresh"
    data = {"knowledgeDB_id": knowledgeDB_id}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# 加载向量库
def load_vector_DB(knowledgeDB_id):
    url = f"{API_BASE_URL}/knowledgeDB/init"
    data = {"knowledgeDB_id": knowledgeDB_id}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# 进行问答
def chat_with_llm(query, session_id, knowledgeDB_id):
    url = f"{API_BASE_URL}/chat/answer"
    data = {"query": query,
            "session_id": session_id,
            "knowledgeDB_id": knowledgeDB_id
    }
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()