# test_stream_with_interrupt.py

from typing import TypedDict
import uuid
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.types import interrupt


# 1. 状态定义
class State(TypedDict):
    email: str


# 2. 节点函数：触发中断
def human_editing_node(state: State):
    print(f"[Node] 当前 email: {state['email']}")
    value = interrupt({
        "text_to_input": state["email"],
        "message": "请输入邮箱地址接收排版文件"
    })
    return {"email": value}


# 3. 构建图
def create_graph():
    builder = StateGraph(State)
    builder.add_node("human_editing_node", human_editing_node)
    builder.add_edge(START, "human_editing_node")
    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)


# 4. 主函数：完全模拟你的真实流式输出逻辑
def main():
    print("🚀 开始测试 LangGraph 流式中断识别")
    print("=" * 60)

    # 创建图
    app = create_graph()

    # 配置 thread_id
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # 初始状态
    initial_state = {"email": "999999@163.com"}
    print(f"🧵 Thread ID: {thread_id}")
    print(f"📥 初始状态: {initial_state}")

    # === 第一阶段：启动流，触发中断 ===
    print("\n🔄 开始流式执行...")
    final_output = None

    for chunk in app.stream(initial_state, config=config, stream_mode="values"):
        print("\n📦 接收到 chunk:")
        print(chunk)

        # ✅ 关键：检查 chunk 是否包含中断
        if isinstance(chunk, dict) and '__interrupt__' in chunk:
            interrupt_data = chunk['__interrupt__']
            print("\n" + "🛑" * 20)
            print("✅ 检测到中断信号！准备暂停流程")
            print(f"中断信息: {interrupt_data}")
            print("🛑" * 20)

            # ✅ 这里你可以 yield 给前端，比如：
            # yield {"awaiting": "user_email", "interrupt_data": interrupt_data}

            # === 模拟：前端返回邮箱后，恢复执行 ===
            print(f"\n💬 模拟前端返回邮箱: '13652001060@163.com'，恢复流程...")
            break  # 跳出循环，准备恢复
        else:
            print("✅ 正常状态更新，继续流式输出...")

    # === 第二阶段：用户输入后，恢复执行 ===
    # 注意：传入 None 或 {}，并使用 Command(resume=...) 恢复
    print("\n🔁 恢复执行，等待最终输出...")

    for chunk in app.stream(
        None,  # 恢复时传 None
        config=config,
        stream_mode="values"
    ):
        print("\n📬 恢复后接收到 chunk:")
        print(chunk)
        final_output = chunk

    print("\n" + "✅" * 20)
    print("最终状态:", final_output)
    print("测试完成！流式中断识别 ✅")
    print("✅" * 20)


# 5. 运行
if __name__ == "__main__":
    main()