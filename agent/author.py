from state.schema import MaingraphState
from tools.utils import zhipu_llm
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from tools.docx_tool import *
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
import re
from typing import List, Dict, Any, Optional
from typing import Optional, Literal

"""（5）作者简介：对文章的全部作者按以下顺序介绍：姓名（出生年-），性别，
籍贯，学历，职称，研究方向。如，张三（1986-），男，吉林长春人，博士，
副教授，主要从事信息资源管理研究。"""

def author_node(state: MaingraphState):
    print(">>>>>> 进入 author 排版节点!!!")

    # agent_mission = state.get("agent_mission", [])
    # layout_check_retrycount = state.get("layout_check_retry", 0)
    #
    # task_details = []
    # required_fields = ["姓名", "性别", "籍贯", "学历", "职称", "研究方向"]
    #
    # for task in agent_mission:
    #     section = task.get("section", "作者信息")
    #     author_text = task.get("author_text", "")
    #     format_requirement = task.get("format_requirement", "")
    #
    #     detected_fields = [field.strip("（）()-0123456789") for field in format_requirement.split("，") if field.strip()]
    #      missing = []
    #     for field in detected_fields:
    #           keyword = field.replace("研究方向", "研究").replace("出生年", "出生").strip()
    #         if keyword not in author_text and len(keyword) > 1:
    #             missing.append(field)
    #
    #     if not missing:
    #         status = "success"
    #         overall_status = "success"
    #         tool_name = "set_author_bio"
    #         tool_args = {
    #             "text": author_text.strip(),
    #             "format_ok": True
    #         }
    #         execution_result = {
    #             "status": "success",
    #             "result": {"message": "作者简介完整，格式符合要求"}
    #         }
    #     else:
    #         status = "failed"
    #         tool_name = "highlight_missing_author_fields"
    #         tool_args = {
    #             "missing_fields": missing,
    #             "suggestion": f"请补充以下信息：{', '.join(missing)}",
    #             "highlight_style": {
    #                 "background_color": "red",
    #                 "color": "white",
    #                 "tag": "<mark>",  # 可执行渲染标记
    #                 "auto_apply": False  # 需人工确认
    #             }
    #         }
    #         execution_result = {
    #             "status": "error",
    #             "error": f"作者简介缺少字段：{', '.join(missing)}"
    #         }
    #
    #     # 构造标准格式输出
    #     task_detail = {
    #         "section": section,
    #         "status": status,
    #         "raw_model_response": format_requirement,
    #         "tool_calls": [
    #             {
    #                 "id": f"call_author_{hash(tuple(missing)) % 10000}",
    #                 "function": {
    #                     "name": tool_name,
    #                     "arguments": json.dumps(tool_args, ensure_ascii=False)
    #                 },
    #                 "type": "tool_call"
    #             }
    #         ],
    #         "tool_execution_results": [
    #             {
    #                 "tool_call_id": f"call_author_{hash(tuple(missing)) % 10000}",
    #                 "tool_name": tool_name,
    #                 "args": tool_args,
    #                 "execution_result": execution_result
    #             }
    #         ]
    #     }
    #     task_details.append(task_detail)
    #
    # # 统计整体状态
    # success_count = sum(1 for t in task_details if t["status"] == "success")
    # total_tasks = len(task_details)
    # overall_status = "success" if success_count == total_tasks else "failed"
    #
    # return {
    #     "author": {
    #         "agent_result": {
    #             "status": overall_status,
    #             "layout_result": task_details
    #         }
    #     },
    #     "agent_done_count": 1,
    #     "layout_check_retry": layout_check_retrycount + 1,
    #     "messages": [
    #         AIMessage(
    #             content=f"【Author Agent】执行完成：{overall_status}，成功 {success_count}/{total_tasks} 项"
    #         )
    #     ],
    # }