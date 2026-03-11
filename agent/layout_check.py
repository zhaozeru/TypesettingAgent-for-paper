from state.schema import MaingraphState
from tools.utils import zhipu_llm, parse_to_json
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, SystemMessage
from config.prompt import layout_check_system_prompt

def layout_check_node(state: MaingraphState):
    system_messages = [
        SystemMessage(content="<-- 进入 05 排版智能中枢Node -->")
    ]
    validation_status = state.get("validation_status") or {}
    validation_notes = state.get("validation_notes", "")

    if validation_status.get("status") == "again":
        system_messages.append(
            SystemMessage(content=">>>>>>   再次进入 05 排版智能中枢Node")
        )
        llm = zhipu_llm(thinking="enabled", temperature=0.2, timeout=120.0)
        fix_plan_prompt = layout_check_system_prompt
        template = ChatPromptTemplate.from_messages(
            [("system", fix_plan_prompt), ("human", "{feedback}")]
        )

        try:
            messages = template.format_messages(feedback=validation_notes)
            response = llm.invoke(messages)
            raw_content = response.content.strip()

            fix_plan = parse_to_json(raw_content)
        except Exception as e:
            system_messages.append(
                SystemMessage(content=f"❌ llm返回结果json化失败: {str(e)}")
            )

        return {
            "update_state": fix_plan,
            "messages": system_messages + [
                AIMessage(content="✅ layout check补漏结束，交给layout_agent！")
            ],
        }
    if validation_status.get("status") == "ok" and state["should_terminate"] is True:
        return {
            "messages": system_messages + [SystemMessage(content="✅ 验证通过，assemble节点！")],
        }

    return {
        "agent_done_count":0,
        "messages": system_messages + [AIMessage(content="✅ 首次执行所以跳过，直接交给layout_agent！")],
    }
