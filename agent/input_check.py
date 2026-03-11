from state.schema import MaingraphState
from config.prompt import input_check_prompt
from langchain_core.prompts import ChatPromptTemplate
from tools.utils import str_to_bool, zhipu_llm
from langchain_core.messages import AIMessage, SystemMessage


def input_check_node(state: MaingraphState):
    llm = zhipu_llm(thinking = 'enabled',temperature = 0.1)
    input_text = state.get("user_input", [])
    input_paper = state.get("paper_file", [])

    template = ChatPromptTemplate.from_messages(
        [("system", input_check_prompt), ("human", "{input}")]
    )
    try:
        response = llm.invoke(template.format_messages(input=input_text))
        raw_result = response.content.strip()
        task_judgement = str_to_bool(raw_result)
    except Exception as e:
        return {
            "task_judgement": False,
            "messages": [
                SystemMessage(content="<-- 进入 01 检查用户输入Node -->"),
                AIMessage(content="模型返回错误，请重试！"),
            ],
        }

    if task_judgement is False:
        return {
            "task_judgement": False,
            "messages": [
                SystemMessage(content="<-- 进入 01 检查用户输入Node -->"),
                AIMessage(content="用户需求超出 agent 任务范围！"),
            ],
        }

    if task_judgement is True and not input_paper:
        return {
            "task_judgement": True,
            "paper_file": None,
            "messages": [
                SystemMessage(content="<-- 进入 01 检查用户输入Node -->"),
                AIMessage(content="用户未上传论文文件！请上传~"),
            ],
        }

    return {
        "task_judgement": True,
        "messages": [
            SystemMessage(content="<-- 进入 01 检查用户输入Node -->"),
            AIMessage(content="符合期刊论文自动排版 agent 任务范围！"),
        ],
    }
