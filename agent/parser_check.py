from state.schema import MaingraphState
from langchain_core.messages import AIMessage, SystemMessage


def parser_check_node(state: MaingraphState):
    input_parser = state["user_input_parser"]
    paper_parser = state["paper_file_parser"]
    # print(">>>>>   ",paper_parser)
    combination = []
    used_subsections = set()

    for item in paper_parser["data"]["result"]:
        subsection = item.get("subsection")
        section = item.get("section")
        item["request"] = []

        if subsection and subsection in input_parser["data"]:
            item["request"] = input_parser["data"][subsection]
            used_subsections.add(subsection)
        elif not subsection and section and section in input_parser["data"]:
            item["request"] = input_parser["data"][section]
            used_subsections.add(section)

        combination.append(item)

    other_request = []
    for key, req in input_parser["data"].items():
        if key not in used_subsections:
            other_request.append({
                "subsection": key,
                "missing_request": req
            })

    if other_request:
        combination.append({
            "section": "其他排版要求",
            "subsection": "未在文档中出现的部分",
            "request": other_request,
        })
    return {
        "request_group": combination,
         "messages": [SystemMessage(content="<-- 进入 04 检查所有解析Node -->"),AIMessage(content="✅ 已将用户输入解析与文章解析内容匹配！")],
    }


