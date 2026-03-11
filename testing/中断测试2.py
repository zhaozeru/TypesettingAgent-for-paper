from typing import TypedDict
import uuid
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
import streamlit as st


# -----------------------------
# 1. 后端：LangGraph 定义
# -----------------------------

class State(TypedDict):
    email: str


def human_editing_node(state: State):
    value = interrupt({
        "text_to_input": state["email"],
        "message": "请输入邮箱地址接收排版文件"
    })
    return {"email": value}


# 创建图（只在第一次运行时初始化）
if 'graph' not in st.session_state:
    graph_builder = StateGraph(State)
    graph_builder.add_node("human_editing_node", human_editing_node)
    graph_builder.add_edge(START, "human_editing_node")
    checkpointer = InMemorySaver()
    st.session_state.graph = graph_builder.compile(checkpointer=checkpointer)

# -----------------------------
# 2. 前端：Streamlit UI
# -----------------------------

# 初始化session state
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = f"user_{uuid.uuid4().hex[:8]}"
if 'interrupt_data' not in st.session_state:
    st.session_state.interrupt_data = None
if 'execution_complete' not in st.session_state:
    st.session_state.execution_complete = False
if 'result' not in st.session_state:
    st.session_state.result = None
if 'execution_started' not in st.session_state:
    st.session_state.execution_started = False
if 'need_human_input' not in st.session_state:
    st.session_state.need_human_input = False

# 主界面
st.title("邮箱输入系统")
st.write("基于LangGraph中断机制的邮箱输入界面")

# 启动按钮 - 只在未开始时显示
if not st.session_state.execution_started and not st.session_state.need_human_input:
    if st.button("开始流程"):
        st.session_state.execution_started = True
        st.rerun()

# 执行流程
if st.session_state.execution_started and not st.session_state.need_human_input and not st.session_state.execution_complete:
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    # 第一次调用，触发中断
    with st.spinner("正在启动流程..."):
        result = st.session_state.graph.invoke(
            {"email": "999999@163.com"},
            config=config
        )

    # 检查是否有中断 - LangGraph的中断数据在 __interrupt__ 属性中
    if hasattr(result, '__interrupt__') or ('__interrupt__' in result if isinstance(result, dict) else False):
        interrupt_obj = getattr(result, '__interrupt__', None) or result.get('__interrupt__', [])

        if interrupt_obj:
            # 提取中断数据
            interrupt_data = interrupt_obj[0].value if hasattr(interrupt_obj[0], 'value') else interrupt_obj[0]
            st.session_state.interrupt_data = interrupt_data
            st.session_state.need_human_input = True
            st.session_state.result = result
            st.rerun()
    else:
        # 如果没有中断，直接完成
        st.session_state.result = result
        st.session_state.execution_complete = True
        st.rerun()

# 显示中断对话框
if st.session_state.need_human_input and st.session_state.interrupt_data:
    st.info("⚠️ 需要用户输入邮箱地址")

    with st.form("email_input_form"):
        st.write(st.session_state.interrupt_data.get("message", "请输入邮箱地址接收排版文件"))

        default_email = st.session_state.interrupt_data.get("text_to_input", "")
        user_email = st.text_input("邮箱地址", value=default_email, key="email_input")

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("提交邮箱")
        with col2:
            cancel = st.form_submit_button("取消")

        if submitted and user_email:
            # 验证邮箱格式（简单验证）
            if "@" in user_email and "." in user_email:
                # 用户提交了邮箱，恢复执行
                config = {"configurable": {"thread_id": st.session_state.thread_id}}

                with st.spinner("正在处理..."):
                    # 使用Command恢复执行
                    command = Command(resume=user_email)
                    final_result = st.session_state.graph.invoke(command, config=config)

                st.session_state.result = final_result
                st.session_state.execution_complete = True
                st.session_state.need_human_input = False
                st.session_state.interrupt_data = None
                st.rerun()
            else:
                st.error("请输入有效的邮箱地址（包含@和.）")

        if cancel:
            st.session_state.need_human_input = False
            st.session_state.interrupt_data = None
            st.session_state.execution_started = False
            st.rerun()

# 显示结果
if st.session_state.execution_complete and st.session_state.result:
    st.success("✅ 流程执行完成！")
    st.write(f"**最终邮箱地址:** {st.session_state.result.get('email', '未知')}")

    if st.button("重新开始"):
        # 重置所有状态
        reset_keys = ['interrupt_data', 'execution_complete', 'result', 'execution_started', 'need_human_input']
        for key in reset_keys:
            if key in st.session_state:
                del st.session_state[key]
        # 重新生成thread_id以确保新的执行流程
        st.session_state.thread_id = f"user_{uuid.uuid4().hex[:8]}"
        st.rerun()

# 显示当前状态（调试信息）
with st.expander("状态信息"):
    st.write(f"**Thread ID:** {st.session_state.thread_id}")
    st.write(f"**执行状态:** {'已开始' if st.session_state.execution_started else '未开始'}")
    st.write(f"**需要人工输入:** {'是' if st.session_state.need_human_input else '否'}")
    st.write(f"**完成状态:** {'已完成' if st.session_state.execution_complete else '未完成'}")

    if st.session_state.interrupt_data:
        st.write("**中断详情:**")
        st.json(st.session_state.interrupt_data)

    if st.session_state.result:
        st.write("**最新结果:**")
        # 安全地显示结果，避免序列化问题
        result_copy = {}
        for key, value in st.session_state.result.items():
            if key != '__interrupt__':  # 跳过中断对象
                result_copy[key] = value
        st.json(result_copy)

        # 单独显示中断信息
        if hasattr(st.session_state.result, '__interrupt__') or '__interrupt__' in st.session_state.result:
            st.write("**中断对象:** (存在但无法直接显示)")

# 使用说明
with st.expander("使用说明"):
    st.markdown("""
    1. 点击 **开始流程** 按钮启动流程
    2. 系统会检测到中断并显示邮箱输入表单
    3. 输入邮箱地址并点击 **提交邮箱**
    4. 查看最终结果
    5. 可以点击 **重新开始** 重新运行流程

    **注意:** 每次重新开始都会生成新的Thread ID，确保独立的执行流程。
    """)