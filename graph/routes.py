from state.schema import MaingraphState
from langgraph.types import Send
from langgraph.constants import END


def routing_func1(state: MaingraphState):
    if state["task_judgement"] == "again":
        return "input_check"
    if state["task_judgement"] is False or not state["paper_file"]:
        return END
    return [Send("input_parser", state), Send("paper_parser", state)]

def routing_func2(state: MaingraphState):
    if state["user_input_parser"]['status'] == "failed":
        return "input_parser"
    if state["input_parser_retry"] >= 3:
        raise ValueError("❌ 用户输入解析陷入循环！")
    if state["user_input_parser"]['status'] == "success":
        return "parser_check"
def routing_func3(state: MaingraphState):
    if state["paper_file_parser"]["status"] == "failed":
        return "paper_parser"
    if state["paper_parser_retry"] >= 3:
        raise ValueError("❌ 文章解析陷入循环！")
    if state["paper_file_parser"]["status"] == "success":
        return "parser_check"


# def routing_func4(state: MaingraphState):
#     if state["layout_check_retry"] == 0 and not state.get("verification_status") and state['should_terminate'] is False:
#         return "layout_agent"
#
#     if state["agent_carry_count"] == state["agent_done_count"] and state['should_terminate'] is False:
#         return "validator"
#     if state["layout_check_retry"] != 0 and state["verification_status"] == "again":
#         return "layout_agent"
#     MAX_LAYOUT_RETRY = 3
#     if state["layout_check_retry"] >= MAX_LAYOUT_RETRY:
#         raise ValueError("❌ 出现循环错误！")
#     if  state["verification_status"] == "ok" and state['should_terminate'] is True:
#         return "assemble"
#     raise ValueError("❌ 有问题！")
def routing_func4(state: MaingraphState):
    retry = state.get("layout_check_retry", 0)
    verification_status = state.get("verification_status")
    should_terminate = state.get("should_terminate", False)
    done_count = state.get("agent_done_count", 0)
    carry_count = state.get("agent_carry_count")
    MAX_RETRY = 3
    if retry >= MAX_RETRY:
        return END

    if retry == 0 and not verification_status and not should_terminate:
        return "layout_agent"

    if verification_status == "again":
        return "layout_agent"

    if carry_count is not None and done_count >= carry_count and not should_terminate:
        return "validator"

    if verification_status == "ok" and should_terminate:
        return "assemble"

    raise ValueError("❌ 有问题！")

def subrouting_func1(state: MaingraphState):
    sends = []
    agent_fields = ["cover", "chart", "author", "fund", "reference", "text","other"]
    for agent_name in agent_fields:
        agent_status = state.get(agent_name, {})
        agent_mission = agent_status.get("agent_mission")
        if agent_mission is not None and len(agent_mission) > 0:
            packet = {
                "agent_mission": agent_mission
            }
            sends.append(Send(agent_name, packet))
    return sends
