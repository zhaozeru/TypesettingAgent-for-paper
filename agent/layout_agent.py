from state.schema import MaingraphState
from typing import  Dict
from langchain_core.messages import AIMessage, SystemMessage
from tools.utils import clean_dict
from config.prompt import layout_agent_rules
def layout_agent_node(state: MaingraphState):
    all_mission = state.get("request_group", [])
    rules = layout_agent_rules
    update: Dict[str, Dict] = {
        "author": {"agent_mission": None, "agent_result": None},
        "chart": {"agent_mission": None, "agent_result": None},
        "cover": {"agent_mission": None, "agent_result": None},
        "fund": {"agent_mission": None, "agent_result": None},
        "reference": {"agent_mission": None, "agent_result": None},
        "text": {"agent_mission": None, "agent_result": None},
        "other": {"agent_mission": None, "agent_result": None},
    }

    for mission in all_mission:
        section = mission.get("section")
        subsection = mission.get("subsection")
        target_key = None

        if subsection:
            for key, keywords in rules.items():
                if subsection in keywords:
                    target_key = key
                    break
        elif section:
            for key, keywords in rules.items():
                if section in keywords:
                    target_key = key
                    break

        if target_key:
            if update[target_key]["agent_mission"] is None:
                update[target_key]["agent_mission"] = []
            update[target_key]["agent_mission"].append(mission)
        else:
            if update["other"]["agent_mission"] is None:
                update["other"]["agent_mission"] = []
            update["other"]["agent_mission"].append(mission)

    filter_update = clean_dict(update)

    return {
        **filter_update,
        "agent_carry_count": len(filter_update),
        "messages": [SystemMessage(content="<-- 进入 06 子图agent分发器 -->"),AIMessage(content="✅ layout agent 任务分发完成！")],
    }
