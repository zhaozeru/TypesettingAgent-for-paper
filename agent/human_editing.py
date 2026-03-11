from state.schema import MaingraphState
from langchain_core.messages import SystemMessage, AIMessage
from langgraph.types import interrupt


def human_editing_node(state: MaingraphState):

    messages = [
        SystemMessage(content="<-- 进入 10 中断输入Node -->"),
        AIMessage(content="✅ 排版已完成！请输入邮箱地址接收排版文件。")
    ]

    value = interrupt({
        "text_to_input": state["email"],
        "message": "请输入邮箱地址接收排版文件"
    })

    return {
        "email": value,
        "messages": messages,
    }