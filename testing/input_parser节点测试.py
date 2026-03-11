from langchain_community.chat_models import ChatZhipuAI
from langchain.prompts import FewShotChatMessagePromptTemplate, ChatPromptTemplate
import re
import json

ZHIPUAI_API_KEY = "f4909101a9ae4b11b9360187bb23e4b5.jhAhTcvXbY4gUWUx"

def zhipu_llm(model: str = "glm-4.5-air", api_key: str = ZHIPUAI_API_KEY, thinking: str = "enabled", stream: bool = True, temperature: float = 0.7, timeout: float = 30.0, **kwargs):
    return ChatZhipuAI(
        api_key=api_key,
        model=model,
        thinking={"type": thinking},
        stream=stream,
        temperature=temperature,
        timeout=timeout,
        **kwargs
    )
def is_empty_rules(rules):
    if not rules:
        return True
    INVALID_VALUES = {"无", "未提及", "", " ", "None", "null", "默认", "常规", "一般"}
    for rule in rules:
        if isinstance(rule, dict):
            for v in rule.values():
                if str(v).strip() not in INVALID_VALUES:
                    return False
    return True
def read_input_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ 文件读取成功！")
        return content
    except Exception as e:
        print(f"❌ 读取失败：{e}")
        return None

# ================== ✅ 新增：默认样式与映射 ==================
DEFAULT_STYLES = {
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

EN_TO_CN_MAPPING = {
        "英文题目": "论文题目",
        "英文作者姓名": "作者姓名",
        "英文作者单位": "作者单位",
        "英文摘要": "摘要",
        "英文关键词": "关键词",
    }
# ============================================================

state = {"user_input": ["C://Users//Administrator//Desktop//用户输入测试.txt"]}
input_parser_paper_sections = [
    "页面布局", "论文题目", "副题目", "作者姓名", "作者单位", "摘要", "关键词", "中图分类号",
    "英文题目", "英文作者姓名", "英文作者单位", "英文摘要", "英文关键词", "正文段落",
    "一级标题", "二级标题", "三级标题", "图表", "公式", "算法", "代码片段", "文献列表",
    "作者简介", "作者贡献声明", "课题或基金项目",
]

input_parser_prompt = """
    用户输入的排版要求：{input}
    请将排版要求按以下论文结构模块分类提取，每个模块用列表形式列出具体规则（如字体、字号、对齐等），未知项可省略或填"无"：
    支持模块：{fields_desc}
    输出格式如下（仅输出 JSON 字典，不要解释）：
    {{
      "论文题目": [
        {{"字体": "XXX"}},
        {{"字号": "XXX"}},
        {{"加粗": "是/否"}},
        {{"对齐": "XXX"}}
      ],
      ...
    }}
    提取结果：
    {output}
"""

input_parser_prompt_examples = [
    {
        "input": "题目黑体三号居中，英文题目也一样但用Times New Roman。摘要宋体小四，英文摘要同中文但字体为Times New Roman。",
        "output": {
            "论文题目": [{"字体": "黑体"}, {"字号": "三号"}, {"对齐": "居中"}],
            "英文题目": [{"字体": "Times New Roman"}, {"字号": "三号"}, {"对齐": "居中"}],
            "摘要": [{"字体": "宋体"}, {"字号": "小四"}],
            "英文摘要": [{"字体": "Times New Roman"}, {"字号": "小四"}]
        }
    }
]

llm2 = zhipu_llm(model="glm-4.5-air", thinking='enabled', temperature=0.1)
input_path = state.get("user_input")[-1]
user_input = read_input_txt(input_path)

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
response = llm2.invoke(extract_input)
raw_content = response.content.strip()
json_match = re.search(r"(\{.*\})", raw_content, re.DOTALL)
if json_match:
    json_str = json_match.group(1)
else:
    print("❌ 未找到有效的 JSON 结构")
    json_str = raw_content

try:
    parsed_data = json.loads(json_str)
    print("✅ LLM 输出已成功解析为字典")
except json.JSONDecodeError as e:
    print(f"❌ JSON 解析失败：{e}")
    print(f"原始输出：\n{raw_content}")
    parsed_data = {}


for en_section, cn_section in EN_TO_CN_MAPPING.items():

    if is_empty_rules(parsed_data.get(en_section)) and not is_empty_rules(parsed_data.get(cn_section)):

        inherited = []
        for rule in parsed_data[cn_section]:
            key = list(rule.keys())[0]
            if key == "字体":
                inherited.append({"字体": "Times New Roman"})
            else:
                inherited.append(rule)
        parsed_data[en_section] = inherited
        print(f"🔗 [Plan B] {en_section} ← 继承自 {cn_section}（用户风格延续）")


for section in input_parser_paper_sections:
    if is_empty_rules(parsed_data.get(section)):
        if section in DEFAULT_STYLES:
            parsed_data[section] = DEFAULT_STYLES[section]
            print(f"📝 [Plan C] {section} ← 使用默认值（兜底保障）")
        else:
            parsed_data[section] = []
            print(f"⚠️  [Plan C] {section} ← 无定义且无默认值")



print(">>>>>> 最终解析结果（含默认值与继承）：")
print(json.dumps(parsed_data, ensure_ascii=False, indent=2))

