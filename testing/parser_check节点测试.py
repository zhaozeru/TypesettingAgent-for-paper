from langchain_community.chat_models import ChatZhipuAI
import docx
import json
import re
from typing import Dict

# 布局规则（未使用，保留）
layout_agent_rules = {
    "cover": [
        "论文题目",
        "副题目",
        "作者姓名",
        "作者单位",
        "摘要",
        "关键词",
        "中图分类号",
        "英文题目",
        "英文作者姓名",
        "英文作者单位",
        "英文摘要",
        "英文关键词",
    ],
    "text": [
        "正文段落",
        "一级标题",
        "二级标题",
        "三级标题",
        "正文",
        "公式",
        "算法",
        "代码片段",
    ],
    "reference": ["文献列表", "参课文献"],
    "fund": ["课题或基金项目", "基金", "基金项目", "横向项目"],
    "chart": ["图片", "表格", "图表"],
    "author": ["作者简介", "作者贡献声明"],
    "other": [],
}

ZHIPUAI_API_KEY = "f4909101a9ae4b11b9360187bb23e4b5.jhAhTcvXbY4gUWUx"


def zhipu_llm(
    model: str = "glm-4.5-air",
    api_key: str = ZHIPUAI_API_KEY,
    thinking: str = "enabled",
    stream: bool = True,
    temperature: float = 0.7,
    timeout: float = 30.0,
    **kwargs,
):
    return ChatZhipuAI(
        api_key=api_key,
        model=model,
        thinking={"type": thinking},
        stream=stream,
        temperature=temperature,
        timeout=timeout,
        **kwargs
    )


def read_json_file(file_path: str) -> Dict:
    """读取 JSON 文件并返回字典"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ JSON 文件读取成功：{file_path}")
        return data
    except FileNotFoundError:
        print(f"❌ 错误：文件未找到 -> {file_path}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解码失败 -> {file_path}：{e}")
    except Exception as e:
        print(f"❌ 读取失败：{e}")
    return {}


def read_txt_file(file_path: str) -> str:
    """读取 TXT 文件并返回字符串"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ TXT 文件读取成功：{file_path}")
        return content
    except Exception as e:
        print(f"❌ TXT 文件读取失败 -> {file_path}：{e}")
        return ""


# 状态：注意这里应该是字符串路径，不是列表
state = {
    "paper_file": r"C:\Users\Administrator\Desktop\论文解析结果.json",  # 修改为字符串
    "user_input": r"C:\Users\Administrator\Desktop\论文首页用户输入解析.txt",  # 修改为字符串
}

# 读取文件
paper_file_path = state["paper_file"]
input_file_path = state["user_input"]

# ✅ 使用正确的函数读取
paper_parser = read_json_file(paper_file_path)  # 必须是 JSON
input_parser = read_json_file(input_file_path)  # 假设你的 .txt 实际上是 JSON 格式保存的
# 如果 .txt 是纯文本而非 JSON，请用 read_txt_file 并做进一步解析

# 如果 input 是纯文本格式，需要你定义格式（比如 JSON 字符串？键值对？），否则无法解析成 dict
# 示例：假设 txt 里是 JSON 字符串
if isinstance(input_parser, dict) and not input_parser:
    # 尝试按文本读取并解析为 JSON
    raw_txt = read_txt_file(input_file_path)
    try:
        input_parser = json.loads(raw_txt)
        print("✅ 成功从文本中解析出 JSON 格式数据")
    except json.JSONDecodeError:
        print("❌ 文本内容不是有效的 JSON 格式，无法解析。")
        input_parser = {"result": {}}

# 开始合并逻辑
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
print(">>>>>>   解析配对完成! ")
# 保存结果
output_file = r"C:\Users\Administrator\Desktop\任务合并结果.json"
try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(combination, f, ensure_ascii=False, indent=4)
    print(f"✅ 论文解析完成！结果已保存至：{output_file}")
except Exception as e:
    print(f"❌ 结果保存失败：{e}")