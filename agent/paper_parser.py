from state.schema import MaingraphState
from tools.utils import zhipu_llm, read_docx, parse_to_json
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, SystemMessage
from config.prompt import paper_parser_system_prompt, paper_parser_paper_sections

def paper_parser_node(state: MaingraphState):
    retry_count = state.get("paper_parser_retry")
    llm = zhipu_llm(thinking='disabled', temperature=0.1, timeout=120.0)
    paper_input = state.get("paper_file")

    try:
        raw_text = read_docx(paper_input)
    except Exception as e:
        return {
            "paper_file_parser": {
                "status": "failed",
                "data": {},
                "error": f"❌ 文件读取失败，原因：{str(e)}",
            },
            "messages": [AIMessage(content=f"❌ 文章读取失败，原因：{str(e)}")],
        }

    system_prompt = paper_parser_system_prompt.format(paper_sections=paper_parser_paper_sections)
    template = ChatPromptTemplate.from_messages(
        [("system",system_prompt), ("human", "{input}")]
    )
    response = llm.invoke(template.format_messages(input=raw_text))
    raw_content = response.content
    try:
        ai_msg_json = parse_to_json(raw_content)
    except Exception as e:
        return {
            "paper_file_parser": {
                "status": "failed",
                "data": {},
                "error": f"❌ 文章LLM → JSON失败，原因：{str(e)}",
            },
            "messages": [AIMessage(content="❌ 论文解析失败，请重试。")],
            "paper_parser_retry": retry_count+1
        }

    return {
        "paper_file_parser": {"status": "success", "data": ai_msg_json},
        "messages": [SystemMessage(content="<-- 进入 03 解析论文Node -->"),AIMessage(content="✅ 已成功解析论文结构，正在准备排版...")],
        "paper_parser_retry": 0
    }

