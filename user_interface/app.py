import streamlit as st
from main import run_formatting_process, app
import tempfile
import uuid
from langgraph.types import Command

# 设置页面
st.set_page_config(
    page_title="期刊论文自动排版助手",
    page_icon="🐮",
    layout="centered",
)

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
if "temp_file_path" not in st.session_state:
    st.session_state["temp_file_path"] = None
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = None
if "process_started" not in st.session_state:
    st.session_state["process_started"] = False
if "process_completed" not in st.session_state:
    st.session_state["process_completed"] = False
if "email_sent" not in st.session_state:
    st.session_state["email_sent"] = False
if "email" not in st.session_state:
    st.session_state["email"] = ""
if "displayed_messages" not in st.session_state:
    st.session_state["displayed_messages"] = set()

# 侧边栏
with st.sidebar:
    st.header("📁 文件上传")

    # 文件上传器
    upload_file = st.file_uploader("选择论文文件", type=["docx"], help="请上传.docx格式的论文文件")
    st.divider()

    # 清理历史记录按钮
    if st.button("🗑️ 清理所有记录", use_container_width=True, type="secondary"):
        # 清除所有会话状态
        keys_to_keep = []  # 不保留任何状态，完全重置
        keys_to_delete = [key for key in st.session_state.keys() if key not in keys_to_keep]
        for key in keys_to_delete:
            del st.session_state[key]
        st.rerun()

# 主内容区域
st.title("🐄 期刊论文自动排版助手")
st.markdown("""> 📝 请输入您的需求，并上传相应文件，Agent将自动为您完成格式排版!  
> **注意**：目前仅支持 `.docx` 格式文件，请确保上传正确类型!""")
st.divider()

# 显示历史消息
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

text_input = st.text_area("排版格式需求", placeholder="请输入您的排版需求，例如：标题居中，正文宋体小四")
if st.button("🚀 开始排版任务"):
    if not text_input.strip() and upload_file is None:
        st.warning("请至少输入需求或上传文件！")
    else:
        user_content = f"📝 排版需求：{text_input}"
        if upload_file:
            user_content += f"\n📎 已上传文件：{upload_file.name}"

        st.session_state["messages"].append({"role": "user", "content": user_content})
        st.session_state["displayed_messages"].add(user_content)

        temp_file_path = None
        if upload_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(upload_file.getvalue())
                temp_file_path = tmp.name

        st.session_state["user_input"] = text_input
        st.session_state["temp_file_path"] = temp_file_path
        st.session_state["thread_id"] = str(uuid.uuid4())
        st.session_state["process_started"] = True
        st.rerun()



# 邮箱输入（在排版完成后显示）
if st.session_state["process_completed"] and not st.session_state["email_sent"]:
    st.header("📧 接收文件")
    email = st.text_input("请输入邮箱地址", value=st.session_state.get("email", ""))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 确认发送", use_container_width=True):
            if "@" not in email:
                st.info("请输入有效的邮箱地址")
            else:
                email_content = f"📧 邮箱地址：{email}"
                st.session_state["email"] = email
                st.session_state["messages"].append({
                    "role": "user",
                    "content": email_content
                })
                st.session_state["displayed_messages"].add(email_content)
                st.session_state["email_sent"] = True
                st.rerun()
    with col2:
        if st.button("❌ 取消", use_container_width=True):
            cancel_content = "您取消了邮件发送。排版流程已终止。"
            st.session_state["messages"].append({
                "role": "assistant",
                "content": cancel_content
            })
            st.session_state["displayed_messages"].add(cancel_content)
            st.session_state["email_sent"] = True
            st.rerun()

# 执行排版流程
if st.session_state["process_started"] and not st.session_state["process_completed"]:
    with st.chat_message("assistant"):
        st.write("🔄 正在启动排版流程...")

    try:
        user_input = st.session_state["user_input"]
        file_path = st.session_state["temp_file_path"]
        thread_id = st.session_state["thread_id"]

        # 执行排版流程
        for chunk in run_formatting_process(user_input, file_path, thread_id):
            # 只处理包含 messages 的 chunk
            if "messages" in chunk:
                for msg in chunk["messages"]:
                    if hasattr(msg, 'content'):
                        content = msg.content
                        # 使用集合去重，避免重复显示相同的消息
                        if content not in st.session_state["displayed_messages"]:
                            st.session_state["messages"].append({"role": "assistant", "content": content})
                            st.session_state["displayed_messages"].add(content)
                            with st.chat_message("assistant"):
                                st.write(content)

        st.session_state["process_completed"] = True
        st.rerun()

    except Exception as e:
        st.error(f"处理失败：{str(e)}")
        st.session_state["process_completed"] = True

# 发送邮件
if st.session_state["email_sent"] and st.session_state["email"]:
    with st.chat_message("assistant"):
        st.write("📤 正在恢复流程并发送邮件...")

    try:
        thread_id = st.session_state["thread_id"]
        email = st.session_state["email"]
        config = {"configurable": {"thread_id": thread_id}}

        for chunk in app.stream(Command(resume=email), config=config, stream_mode="values"):
            # 只处理包含 messages 的 chunk
            if "messages" in chunk:
                for msg in chunk["messages"]:
                    if hasattr(msg, 'content'):
                        content = msg.content
                        # 使用集合去重，避免重复显示相同的消息
                        if content not in st.session_state["displayed_messages"]:
                            st.session_state["messages"].append({"role": "assistant", "content": content})
                            st.session_state["displayed_messages"].add(content)
                            with st.chat_message("assistant"):
                                st.write(content)

    except Exception as e:
        st.error(f"恢复执行失败：{str(e)}")