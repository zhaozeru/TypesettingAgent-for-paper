from state.schema import MaingraphState
from tools.utils import zhipu_llm
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from tools.docx_tool import *
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.tools import tool
import re
from typing import List, Dict, Any, Optional
from typing import Optional, Literal


def extract_changes_made(content: str) -> str:
    start = content.find("**已完成操作**：")
    if start == -1:
        return "未知操作"
    return content[start:].strip()

def cover_node(state: MaingraphState):
    system_messages = [
        SystemMessage(content="<-- 进入 07 首页 Agent 排版 Node -->")
    ]

    layout_check_retrycount = state.get("layout_check_retry",0)
    tools = [
        set_font_name,
        set_font_size,
        set_font_bold,
        set_font_italic,
        set_paragraph_align,
        set_line_spacing,
        set_paragraph_indent,
        #
        check_title_length,
        check_keyword_count,
        check_abstract_structure,
        check_abstract_length,
        check_author_affiliation_by_llm,
        check_author_name_format,
    ]
    tool_lookup = {tool.name: tool for tool in tools}

    llm = zhipu_llm(
        thinking="enabled", temperature=0.3, timeout=240.0, model="glm-4.5-air"
    )
    llm_with_tools = llm.bind_tools(tools)
    system_prompt = """
    你是一个专业、严格的格式解析大师，负责将排版任务转换为代码参数，以支持后续的工具调用。

    ## 任务说明
    - 你会接收到一个包含全部信息的任务详情，请你全面理解该任务
    - 然后，你需要理解用户具体的排版要求，并了解所有工具任务能力、需要的参数和参数格式
    - 要做的就是为每一个排版要求选择合适的执行工具，并将要求转换成工具可以执行的参数格式
    - 最后，你只能通过调用工具来完成任务，不能返回其他解释或文字。

    ## 示例输入：
    {{
        "section": "首页",
        "subsection": "论文题目",
        "content": "基于《金匮要略》的多粒度知识表示模型构建研究",
        "request": [
          {{"字体": "黑体"}},
          {{"字号": "二号"}},
          {{"加粗": "是"}}
        ]
    }}
    ## 输出规则
    - 你只能通过 tool call 执行操作
    - 不要输出思考过程、说明、总结或自然语言解释
    - 输出：直接生成 tool calls。
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "请根据以下任务生成对应的格式化指令：\n{mission}"),
        ]
    )

    task_details = []

    for idx, task in enumerate(state.get("agent_mission", [])):
        # system_messages.append(SystemMessage(content=f"\n🔄 正在处理任务 {idx + 1}: {task['section']} > {task['subsection']}"))
        input_messages = prompt.format_messages(mission=json.dumps(task, ensure_ascii=False))

        try:
            response = llm_with_tools.invoke(input_messages)
            # system_messages.append(SystemMessage(content=f"🟢 response 类型: {type(response)}"))


            tool_calls = getattr(response, "tool_calls", []) or []
            raw_content = getattr(response, "content", "").strip() if isinstance(getattr(response, "content", ""),str) else ""

            execution_results = []

            for tc in tool_calls:
                if not isinstance(tc, dict):
                    execution_results.append({
                        "tool_call_id": None,
                        "tool_name": "unknown",
                        "args": {},
                        "execution_result": {"status": "error", "error": f"无效 tool_call 类型: {type(tc)}"}
                    })
                    continue

                name = tc.get("name")
                args = tc.get("args", {})

                if name not in tool_lookup:
                    error = f"工具未注册: {name}，可用: {list(tool_lookup.keys())}"
                    execution_results.append({
                        "tool_call_id": tc.get("id"),
                        "tool_name": name,
                        "args": args,
                        "execution_result": {"status": "error", "error": error}
                    })
                else:
                    try:
                        result = tool_lookup[name].invoke(args)
                        execution_results.append({
                            "tool_call_id": tc.get("id"),
                            "tool_name": name,
                            "args": args,
                            "execution_result": {"status": "success", "result": result}
                        })
                    except Exception as e:
                        execution_results.append({
                            "tool_call_id": tc.get("id"),
                            "tool_name": name,
                            "args": args,
                            "execution_result": {"status": "error", "error": str(e)}
                        })

            if not tool_calls:
                status = "failed"
            else:
                success_count = sum(1 for r in execution_results if r["execution_result"]["status"] == "success")
                status = "success" if success_count == len(execution_results) else "failed"

            task_detail = {
                "section": task["section"],
                "subsection": task["subsection"],
                "status": status,
                "raw_model_response": raw_content,
                "tool_calls": tool_calls,
                "tool_execution_results": execution_results,
            }
            task_details.append(task_detail)
            # system_messages.append(SystemMessage(content=f"✅ {task['subsection']} 处理完成，状态: {status}"))


        except Exception as e:
            system_messages.append(SystemMessage(content=f"❌ 处理失败: {task['subsection']} | {str(e)}"))
            task_details.append({
                "section": task["section"],
                "subsection": task["subsection"],
                "status": "error",
                "raw_model_response": f"调用异常: {str(e)}",
                "tool_calls": [],
                "tool_execution_results": [],
            })

    success_count = sum(1 for t in task_details if t["status"] == "success")
    total_tasks = len(task_details)
    overall_status = (
        "success"
        if success_count == total_tasks and total_tasks > 0
        else "partial_success" if success_count > 0 else "failed"
    )

    return {
        "cover": {
            "agent_result": {
                "status": overall_status,
                "layout_result": task_details
            }
        },
        "agent_done_count": 1,
        "layout_check_retry": layout_check_retrycount + 1,
        "messages": system_messages + [
            AIMessage(
                content=f"【Cover Agent】执行完成：{overall_status}，成功 {success_count}/{total_tasks} 项"
            )
        ],
    }
