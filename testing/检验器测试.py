from typing import List, Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.prebuilt import create_react_agent
import json
from langchain_community.chat_models import ChatZhipuAI

state2 = {
    "cover": {
        "agent_result": {
            "status": "partial_success",
            "layout_result":
                [
                    # --- 任务1：设置论文题目（成功）---
                    {
                        "section": "首页",
                        "subsection": "论文题目",
                        "status": "success",
                        "raw_model_response": "",  # 因为 prompt 要求不输出解释
                        "tool_calls": [
                            {
                                "id": "call_123",
                                "function": {
                                    "name": "set_font_name",
                                    "arguments": '{"font_name": "黑体"}',
                                },
                                "type": "tool_call",
                            },
                            {
                                "id": "call_124",
                                "function": {
                                    "name": "set_font_size",
                                    "arguments": '{"font_size": 22}',
                                },
                                "type": "tool_call",
                            },
                            {
                                "id": "call_125",
                                "function": {
                                    "name": "set_font_bold",
                                    "arguments": '{"bold": true}',
                                },
                                "type": "tool_call",
                            },
                        ],
                        "tool_execution_results": [
                            {
                                "tool_call_id": "call_123",
                                "tool_name": "set_font_name",
                                "args": {"font_name": "黑体"},
                                "execution_result": {
                                    "status": "success",
                                    "result": {
                                        "applied": True,
                                        "target": "title",
                                        "message": "字体已设为黑体",
                                    },
                                },
                            },
                            {
                                "tool_call_id": "call_124",
                                "tool_name": "set_font_size",
                                "args": {"font_size": 22},
                                "execution_result": {
                                    "status": "success",
                                    "result": {
                                        "applied": True,
                                        "target": "title",
                                        "message": "字号已设为二号（22pt）",
                                    },
                                },
                            },
                            {
                                "tool_call_id": "call_125",
                                "tool_name": "set_font_bold",
                                "args": {"bold": True},
                                "execution_result": {
                                    "status": "success",
                                    "result": {
                                        "applied": True,
                                        "target": "title",
                                        "message": "已加粗",
                                    },
                                },
                            },
                        ],
                    },
                    # --- 任务2：检查摘要长度（失败）---
                    {
                        "section": "首页",
                        "subsection": "摘要",
                        "status": "failed",
                        "raw_model_response": "**已完成操作**：调用 check_abstract_length 工具检测摘要长度。",
                        "tool_calls": [
                            {
                                "id": "call_456",
                                "function": {
                                    "name": "check_abstract_length",
                                    "arguments": "{}",
                                },
                                "type": "tool_call",
                            }
                        ],
                        "tool_execution_results": [
                            {
                                "tool_call_id": "call_456",
                                "tool_name": "check_abstract_length",
                                "args": {},
                                "execution_result": {
                                    "status": "error",
                                    "error": "摘要长度仅为 80 字，低于最低要求 300 字。",
                                },
                            }
                        ],
                    },
                ]
            ,
        }
    },

}
state1 = {
    "agent_mission": [
      {
        "section": "首页",
        "subsection": "论文题目",
        "content": "基于《金匮要略》的多粒度知识表示模型构建研究",
        "request": [
          {"字体": "黑体"},
          {"字号": "二号"},
          {"加粗": "是"}
        ]
      },
      {
        "section": "首页",
        "subsection": "摘要",
        "content": "[目的] 本文基于多粒度层级划分提出多粒度的知识表示框架与模型，以提升中医古籍知识挖掘与利用效率。[方法] 本文首先通过对《金匮要略》的分析与归纳提出从知识内容角度出发的多粒度层级划分结构。然后，据此构建出中医古籍多粒度知识表示框架，并给出多粒度知识表示模型，并以《金匮要略》和《温病条辨》中的知识内容进行了模型展示与验证。[结果] 对多粒度知识表示模型的应用，展示出模型的普适性和科学性，体现出模型在中医古籍领域中的可用性和有效性，有效支持中医古籍知识表示与组织。",
        "request": [
          {"字体": "宋体"},
          {"字号": "小四"},
          {"斜体": "是"}
        ]
      }
    ]
}

ZHIPUAI_API_KEY ="f4909101a9ae4b11b9360187bb23e4b5.jhAhTcvXbY4gUWUx"
def zhipu_llm(model: str = 'glm-4.5-air',api_key: str = ZHIPUAI_API_KEY,thinking: str = 'enabled',stream: bool = True,temperature: float = 0.7,timeout: float = 30.0,**kwargs):
    return ChatZhipuAI(
        api_key=api_key,
        model=model,
        thinking={
            "type": thinking,
        },
        stream=stream,
        temperature=temperature,
        timeout=timeout,
        **kwargs
    )
llm = ChatZhipuAI(
    api_key=ZHIPUAI_API_KEY,
    model="glm-4.5-air",
    temperature=0.3,
    timeout=120.0
)
system_prompt = """
你是一个专业的排版合规性审查大师。请根据用户的排版要求，审查实际执行结果。

请判断每一项是否真正满足要求（不能只看工具调用是否成功），若失败请说明原因。

输出格式示例：
{{
    "verification_result": [
        {{
            "section": "首页",
            "subsection": "论文题目",
            "request": {{"字体": "黑体", "字号": "二号", "加粗": "是"}},
            "status": "success|failed",
            "reason": "详细说明"
        }}
    ],
    "overall_status": "success|partial_success|failed"
}}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "请审查以下任务的执行情况：\n{task_and_result}")
])



verification_results = []


exec_map = {
    (item["section"], item["subsection"]): item
    for item in state2.get("cover", {}).get("agent_result", {}).get("layout_result", [])
}

for mission in state1["agent_mission"]:
    sec = mission["section"]
    subsec = mission["subsection"]
    request = {k: v for req in mission["request"] for k, v in req.items()}

    exec_result = exec_map.get((sec, subsec))
    if not exec_result:
        verification_results.append({
            "section": sec,
            "subsection": subsec,
            "request": request,
            "status": "failed",
            "reason": "该任务未被执行（无执行记录）"
        })
        continue

    input_data = {
        "original_request": mission,
        "execution_result": exec_result
    }

    try:

        response = llm.invoke(
            prompt.format(task_and_result=json.dumps(input_data, ensure_ascii=False, indent=2))
        )
        content = response.content.strip()

        # 清理 Markdown 代码块标记
        if content.startswith("```json"):
            content = content[7:-3].strip()

        result_json = json.loads(content)


        if isinstance(result_json.get("verification_result"), list) and len(result_json["verification_result"]) > 0:
            item = result_json["verification_result"][0]
            verification_results.append({
                "section": item.get("section", sec),
                "subsection": item.get("subsection", subsec),
                "request": request,
                "status": item.get("status", "failed"),
                "reason": item.get("reason", "未知错误")
            })
        else:
            verification_results.append({
                "section": sec,
                "subsection": subsec,
                "request": request,
                "status": "failed",
                "reason": f"模型返回格式错误: {content}"
            })

    except Exception as e:
        verification_results.append({
            "section": sec,
            "subsection": subsec,
            "request": request,
            "status": "failed",
            "reason": f"审查调用失败: {str(e)}"
        })


verification_success_result = [r for r in verification_results if r["status"] == "success"]
verification_failed_result = [r for r in verification_results if r["status"] == "failed"]


if all(r["status"] == "success" for r in verification_results):
    verification_status = "success"
    should_terminate = True
elif len(verification_success_result) > 0:
    verification_status = "partial_success"
    should_terminate = False
else:
    verification_status = "failed"
    should_terminate = False


final_output = {
    "verification_status": verification_status,
    "should_terminate": should_terminate,
    "verification_success_result": verification_success_result,
    "verification_failed_result": verification_failed_result,
}
print(json.dumps(final_output, ensure_ascii=False, indent=2))
