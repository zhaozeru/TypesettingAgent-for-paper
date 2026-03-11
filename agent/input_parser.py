from state.schema import MaingraphState
from tools.utils import zhipu_llm, parse_to_json
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
from langchain_core.messages import AIMessage,SystemMessage
from config.prompt import input_parser_prompt, input_parser_prompt_examples, input_parser_paper_sections
def is_empty_rules(rules):
    if not rules:
        return True
    INVALID_VALUES = {"无", "未提及", "", " ", "None", "null"}
    for rule in rules:
        if isinstance(rule, dict):
            for v in rule.values():
                if str(v).strip() not in INVALID_VALUES:
                    return False
    return True

# 后续要加上对文档的识别，因为有的期刊将论文模版以模版形式发布，用户会上传文档作为要求
def input_parser_node(state:MaingraphState):
    default_styles = {
        "论文题目": [{"字体": "黑体"}, {"字号": "三号"}, {"加粗": "是"}, {"对齐": "居中"}],
        "作者姓名": [{"字体": "宋体"}, {"字号": "小四"}, {"对齐": "居中"}],
        "作者单位": [{"字体": "宋体"}, {"字号": "五号"}, {"对齐": "居中"}],
        "摘要": [{"字体": "宋体"}, {"字号": "小四"}, {"行距": "1.5倍"}, {"段落格式": "首行缩进2字符"}],
        "关键词": [{"字体": "宋体"}, {"字号": "五号"}, {"行距": "1.5倍"}],
        "中图分类号": [{"字体": "宋体"}, {"字号": "五号"}],
        "英文题目": [{"字体": "Times New Roman"}, {"字号": "三号"}, {"加粗": "是"}, {"对齐": "居中"}],
        "英文作者姓名": [{"字体": "Times New Roman"}, {"字号": "小四"}, {"对齐": "居中"}],
        "英文作者单位": [{"字体": "Times New Roman"}, {"字号": "五号"}, {"对齐": "居中"}],
        "英文摘要": [{"字体": "Times New Roman"}, {"字号": "小四"}, {"行距": "1.5倍"}, {"段落格式": "首行缩进2字符"}],
        "英文关键词": [{"字体": "Times New Roman"}, {"字号": "五号"}, {"行距": "1.5倍"}],
        "正文段落": [{"字体": "宋体"}, {"字号": "小四"}, {"行距": "1.5倍"}, {"段落格式": "首行缩进2字符"}],
        "一级标题": [{"字体": "黑体"}, {"字号": "三号"}, {"加粗": "是"}, {"对齐": "居中"}, {"段前段后": "各12pt"}],
        "二级标题": [{"字体": "黑体"}, {"字号": "四号"}, {"加粗": "是"}, {"对齐": "左对齐"}, {"段前段后": "各6pt"}],
        "三级标题": [{"字体": "楷体"}, {"字号": "小四"}, {"加粗": "是"}, {"对齐": "左对齐"}],
    }
    en_to_cn_mapping = {
        "英文题目": "论文题目",
        "英文作者姓名": "作者姓名",
        "英文作者单位": "作者单位",
        "英文摘要": "摘要",
        "英文关键词": "关键词",
    }
    system_messages = [
        SystemMessage(content="<-- 进入 02 解析用户输入 Node -->")
    ]
    llm = zhipu_llm(thinking='disabled', temperature=0.1)
    user_input = state.get("user_input")
    retry_count = state.get("input_parser_retry")
    paper_sections = input_parser_paper_sections

    example_prompt = ChatPromptTemplate.from_template(input_parser_prompt).partial(fields_desc=", ".join(paper_sections))
    examples = input_parser_prompt_examples
    extract_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是一个论文排版规则提取与推理专家。\n"
                "请根据输入的排版要求，按以下模块分类提取结构化规则：\n"
                f"{', '.join(input_parser_paper_sections)}\n\n"
                "要求：\n"
                "- 每个模块用列表返回多个属性，格式为 {{'key': 'value'}}\n"
                "- 对于明确提到的规则，请直接提取；\n"
                "- 对于未明确说明但可合理推断的规则（如英文通常用 Times New Roman），请进行推断。\n"
                "- 若某类目完全无信息，则返回空列表 []，或填 '无'！\n"
                "- 不要添加额外解释或说明。\n"
                "- 输出必须是纯 JSON 字典格式，仅包含字段和规则列表。\n"
            ),
            FewShotChatMessagePromptTemplate(example_prompt=example_prompt, examples=examples),
            ("human", "{input}"),
        ]
    )

    extract_input = extract_prompt.invoke({"input": user_input})
    response = llm.invoke(extract_input)
    raw_content = response.content.strip()
    parsed_data = parse_to_json(raw_content)
    if not parsed_data:
        system_messages.append(SystemMessage(content="❌ 用户问题解析提取失败！"))
        return {
            "user_input_parser": {
                "status": "failed",
                "data": "",
                "error": "用户问题解析提取失败！！！",
            },
            "rejection_reason": "input_parser_node 用户问题解析提取失败!",
            "messages": system_messages + [AIMessage(content="解析失败，请检查输入。")],
            "input_parser_retry": retry_count + 1
        }

    for en_section, cn_section in en_to_cn_mapping.items():
        if is_empty_rules(parsed_data.get(en_section)) and not is_empty_rules(parsed_data.get(cn_section)):
            inherited = []
            for rule in parsed_data[cn_section]:
                key = list(rule.keys())[0]
                if key == "字体":
                    inherited.append({"字体": "Times New Roman"})
                else:
                    inherited.append(rule)
            parsed_data[en_section] = inherited
            # system_messages.append(
            #     SystemMessage(content=f"🔗 [Plan B] {en_section} ← 继承自 {cn_section}（用户风格延续）")
            # )

    for section in input_parser_paper_sections:
        if is_empty_rules(parsed_data.get(section)):
            if section in default_styles:
                parsed_data[section] = {
                    "items": default_styles[section],
                    "source": "system_default"
                }
                # system_messages.append(
                #     SystemMessage(content=f"📝 [Plan C] {section} ← 使用默认值（兜底保障）")
                # )
            else:
                parsed_data[section] = {
                    "items": [],
                    "source": "system_default"
                }
                # system_messages.append(
                #     SystemMessage(content=f"⚠️  [Plan C] {section} ← 无定义且无默认值")
                # )


    return {
        "user_input_parser": {"status": "success", "data": parsed_data},
        "messages": system_messages + [AIMessage(content="用户输入解析完成！")],
        "input_parser_retry": 0,
    }
