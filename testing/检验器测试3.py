from ..state.schema import MaingraphState
from ..tools.utils import zhipu_llm
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
import json
from ..config.prompt import validator_system_prompt


def validator_node(state: MaingraphState):
    print(">>>>>>   进入 08 检验器节点!!! ")

    llm = zhipu_llm(model="glm-4.5-air", temperature=0.3, timeout=120.0)
    system_prompt = validator_system_prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "请审查以下任务的执行情况：\n{task_and_result}"),
        ]
    )

    verification_results = []
    agents = ["author", "chart", "cover", "fund", "reference", "text", "other"]
    for agent_name in agents:
        agent_state = state.get(agent_name)
        if not agent_state:
            continue
        missions = agent_state.get("agent_mission", [])
        results = agent_state.get("agent_result", {}).get("layout_result", [])
        exec_map = {(item["section"], item["subsection"]): item for item in results}

        for mission in missions:
            sec = mission["section"]
            subsec = mission["subsection"]
            request = {k: v for req in mission["request"] for k, v in req.items()}

            exec_result = exec_map.get((sec, subsec))
            if not exec_result:
                verification_results.append(
                    {
                        "agent_name": agent_name,
                        "section": sec,
                        "subsection": subsec,
                        "request": request,
                        "status": "failed",
                        "reason": f"[{agent_name}] 该任务未被执行（无执行记录）",
                    }
                )
                continue
            input_data = {"original_request": mission, "execution_result": exec_result}
            try:
                response = llm.invoke(
                    prompt.format(
                        task_and_result=json.dumps(
                            input_data, ensure_ascii=False, indent=2
                        )
                    )
                )
                content = response.content.strip()
                if content.startswith("```json"):
                    content = content[7:-3].strip()

                result_json = json.loads(content)
                if (
                    isinstance(result_json.get("verification_result"), list)
                    and len(result_json["verification_result"]) > 0
                ):
                    item = result_json["verification_result"][0]
                    verification_results.append(
                        {
                            "agent_name": agent_name,
                            "section": item.get("section", sec),
                            "subsection": item.get("subsection", subsec),
                            "request": request,
                            "status": item.get("status", "failed"),
                            "reason": item.get("reason", "未知错误"),
                        }
                    )
                else:
                    verification_results.append(
                        {
                            "agent_name": agent_name,
                            "section": sec,
                            "subsection": subsec,
                            "request": request,
                            "status": "failed",
                            "reason": f"[{agent_name}] 模型返回格式错误: {content}",
                        }
                    )

            except Exception as e:
                verification_results.append(
                    {
                        "agent_name": agent_name,
                        "section": sec,
                        "subsection": subsec,
                        "request": request,
                        "status": "failed",
                        "reason": f"[{agent_name}] 审查调用失败: {str(e)}",
                    }
                )

    verification_success_result = [
        r for r in verification_results if r["status"] == "success"
    ]
    verification_failed_result = [
        r for r in verification_results if r["status"] == "failed"
    ]

    if all(r["status"] == "success" for r in verification_results):
        verification_status = "ok"
        should_terminate = True
    elif len(verification_success_result) > 0:
        verification_status = "again"
        should_terminate = False
    else:
        verification_status = "again"
        should_terminate = False

    print(">>>>>>   检验器校验完毕！")
    return {
        "verification_status": verification_status,
        "should_terminate": should_terminate,
        "verification_success_result": verification_success_result,
        "verification_failed_result": verification_failed_result,
        "messages": [AIMessage(content=f"✅ 检验器校验结束，总体检验结果：{verification_status}")],
    }
