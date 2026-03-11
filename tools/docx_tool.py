from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.tools import tool
import json
import re
from typing import Optional, Literal, Dict, Any
from tools.utils import zhipu_llm

# 检查类工具
@tool
def check_title_length(title: str, max_chars: int = 20) -> dict:
    """
    检查论文或文章的中文标题长度是否超过指定字数。
    Args:
        title (str): 中文标题
        max_chars (int): 最大允许汉字数，默认20
    Returns:
        dict: 检查结果
    """
    char_count = len([c for c in title if '\u4e00' <= c <= '\u9fff'])

    if char_count <= max_chars:
        return {
            "status": "success",
            "type": "check",
            "data": {
                "result": True,
                "check_name": "题目长度",
                "message": f"标题长度合规：{char_count} 字（≤{max_chars}）",
                "severity": "info"
            }
        }
    else:
        return {
            "status": "failed",
            "type": "check",
            "data": {
                "result": False,
                "check_name": "题目长度",
                "message": f"标题过长：{char_count} 字（超过{max_chars}字限制）",
                "severity": "error",
                # 修订注释信息
                "revision_comment": {
                    "author": "格式检查器",
                    "text": f"标题长度超过限制：当前{char_count}字，限制{max_chars}字",
                    "paragraph_index": None,  # 将在组装节点中设置
                    "run_index": None  # 将在组装节点中设置
                }
            }
        }
@tool
def check_keyword_count(keywords: str, min_count: int = 3, max_count: Optional[int] = 8,separators: str = r';|；|,|，|\s*\n\s*|\s{2,}') -> Dict[str, Any]:
    """
    检查关键词数量（支持中英文）
    Args:
        keywords (str): 中文关键词字符串，如 "情报学；应急管理，互联网医疗"
        min_count (int): 最少数量，默认3
        max_count (int, optional): 最多数量，默认8
        separators (str): 正则表达式，用于匹配分隔符，默认支持：中文/英文分号、逗号、空格、换行等

    Returns:
        dict: 检查结果
    """
    keyword_list = [
        kw.strip() for kw in re.split(separators, keywords.strip()) if kw.strip()
    ]
    count = len(keyword_list)

    if max_count is not None:
        result = min_count <= count <= max_count
    else:
        result = count >= min_count

    if result:
        return {
            "status": "success",
            "type": "check",
            "data": {
                "result": True,
                "check_name": "关键词数量",
                "message": f"关键词数量合规：{count} 个",
                "severity": "info",
                "details": {
                    "count": count,
                    "keywords_list": keyword_list,
                }
            }
        }
    else:
        if count < min_count:
            message = f"关键词数量不足：{count} 个（至少需要 {min_count} 个）"
        else:
            message = f"关键词数量过多：{count} 个（建议不超过 {max_count} 个）"

        return {
            "status": "failed",
            "type": "check",
            "data": {
                "result": False,
                "check_name": "关键词数量",
                "message": message,
                "severity": "error",
                "details": {
                    "count": count,
                    "keywords_list": keyword_list,
                },
                "revision_comment": {
                    "author": "格式检查器",
                    "text": message,
                    "paragraph_index": None,
                    "run_index": None
                }
            }
        }
@tool
def check_abstract_structure(abstract: str,required_sections: list = ["目的/意义", "方法/过程", "结果/结论", "创新/局限"],optional_sections: list = []) -> dict:
    """
    检查摘要是否包含规定的结构化内容部分，基于内容语义而非格式标签。
    """
    # 定义中英文关键词映射，用于检测各个部分的内容
    section_keywords = {
        "目的/意义": ["目的", "意义", "目标", "旨在", "为了", "purpose", "objective", "aim", "goal"],
        "方法/过程": ["方法", "过程", "采用", "通过", "利用", "基于", "method", "approach", "procedure", "using"],
        "结果/结论": ["结果", "结论", "发现", "表明", "显示", "result", "finding", "conclusion", "show", "demonstrate"],
        "创新/局限": ["创新", "局限", "贡献", "不足", "创新性", "局限性", "innovation", "contribution", "limitation",
                      "novelty"]
    }

    found = []
    missing = []
    abstract_text = abstract.strip().lower()

    for section in required_sections:
        keywords = section_keywords.get(section, [section.lower()])
        matched = False

        # 检查是否包含该部分的关键词
        for keyword in keywords:
            if keyword in abstract_text:
                found.append(section)
                matched = True
                break

        if not matched:
            missing.append(section)

    result = len(missing) == 0

    if result:
        return {
            "status": "success",
            "type": "check",
            "data": {
                "result": True,
                "check_name": "摘要结构检查",
                "message": "摘要结构完整，包含所有必要部分",
                "severity": "info",
                "details": {
                    "found_sections": found,
                    "missing_sections": missing
                }
            }
        }
    else:
        return {
            "status": "failed",
            "type": "check",
            "data": {
                "result": False,
                "check_name": "摘要结构检查",
                "message": f"摘要缺少以下内容部分：{', '.join(missing)}",
                "severity": "error",
                "details": {
                    "found_sections": found,
                    "missing_sections": missing
                },
                "revision_comment": {
                    "author": "内容检查器",
                    "text": f"摘要内容不完整，缺少：{', '.join(missing)} 部分",
                    "paragraph_index": None,
                    "run_index": None
                }
            }
        }
@tool
def check_abstract_length(abstract: str, target_words: int = 400,tolerance: int = 200, unit: str = "chars") -> Dict[str, Any]:
    """
    检查摘要长度是否在目标范围内，支持中英文。
    """
    text = abstract.strip()
    if not text:
        char_count = word_count = 0
    else:
        char_count = len([c for c in text if "\u4e00" <= c <= "\u9fff"])
        words = re.findall(r"[a-zA-Z]+", text)
        word_count = len(words)

    if unit == "auto":
        unit = "chars" if char_count > word_count else "words"

    if unit == "words":
        count = word_count
        unit_label = "词"
    else:
        count = char_count
        unit_label = "字"

    lower = target_words - tolerance
    upper = target_words + tolerance

    if lower <= count <= upper:
        return {
            "status": "success",
            "type": "check",
            "data": {
                "result": True,
                "check_name": "摘要长度",
                "message": f"摘要长度合规：{count}{unit_label}（目标 {target_words}±{tolerance}）",
                "severity": "info",
                "details": {
                    "count": count,
                    "unit": unit,
                    "target_range": f"{lower}-{upper}"
                }
            }
        }
    elif count < lower:
        message = f"摘要过短：{count}{unit_label}（建议至少 {lower} {unit_label}）"
        severity = "warning"
    else:
        message = f"摘要过长：{count}{unit_label}（建议不超过 {upper} {unit_label}）"
        severity = "warning"

    return {
        "status": "failed",
        "type": "check",
        "data": {
            "result": False,
            "check_name": "摘要长度",
            "message": message,
            "severity": severity,
            "details": {
                "count": count,
                "unit": unit,
                "target_range": f"{lower}-{upper}"
            },
            "revision_comment": {
                "author": "格式检查器",
                "text": message,
                "paragraph_index": None,
                "run_index": None
            }
        }
    }
@tool
def check_author_affiliation_by_llm(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    使用大模型检查作者及作者单位的格式是否符合用户的具体要求。

    输入 state 包含：
        - requirement: 用户的具体格式要求
        - content_to_check: 待检查的文本（作者+单位信息）

    Returns:
        dict: 检查结果，格式与其他检查工具一致
    """
    requirement = state.get("requirement", "").strip()
    content = state.get("content_to_check", "").strip()

    if not content:
        return {
            "status": "failed",
            "type": "check",
            "data": {
                "result": False,
                "check_name": "作者单位格式检查",
                "message": "缺少待检查的作者单位内容",
                "severity": "error",
                "revision_comment": {
                    "author": "格式检查器",
                    "text": "缺少作者单位信息，请补充完整",
                    "paragraph_index": None,
                    "run_index": None
                }
            }
        }

    if not requirement:
        # 如果没有具体要求，使用默认的学术规范作为参考
        requirement = "符合学术论文的作者和单位格式规范"

    # 根据用户要求进行检查的提示词
    prompt_template = """
请根据以下具体要求判断作者和单位信息格式是否符合要求：

【用户要求】
{requirement}

【待检查内容】
{content}

请判断是否符合要求，并简要说明原因（如不符合）。
只返回：符合 或 不符合+原因
"""

    try:
        prompt = prompt_template.format(
            requirement=requirement,
            content=content
        )
        llm = zhipu_llm(
            thinking="enabled", temperature=0.1, timeout=120.0
        )
        response = llm.invoke(prompt)
        raw_output = response.content.strip()

        # 解析模型响应
        if "符合" in raw_output and "不符合" not in raw_output:
            return {
                "status": "success",
                "type": "check",
                "data": {
                    "result": True,
                    "check_name": "作者单位格式检查",
                    "message": f"作者单位格式符合要求：{requirement}",
                    "severity": "info"
                }
            }
        else:
            # 提取不符合的原因
            if "不符合" in raw_output:
                reason = raw_output.split("不符合")[1].strip()
            else:
                reason = "格式不符合用户要求"

            # 限制原因长度
            reason = reason[:30] + "..." if len(reason) > 30 else reason

            return {
                "status": "failed",
                "type": "check",
                "data": {
                    "result": False,
                    "check_name": "作者单位格式检查",
                    "message": f"作者单位格式不符合要求：{reason}",
                    "severity": "error",
                    "revision_comment": {
                        "author": "格式检查器",
                        "text": f"作者单位格式问题：{reason}",
                        "paragraph_index": None,
                        "run_index": None
                    }
                }
            }

    except Exception as e:
        return {
            "status": "failed",
            "type": "check",
            "data": {
                "result": False,
                "check_name": "作者单位格式检查",
                "message": f"检查过程中发生错误: {str(e)}",
                "severity": "error",
                "revision_comment": {
                    "author": "格式检查器",
                    "text": "检查工具执行异常，请手动验证格式",
                    "paragraph_index": None,
                    "run_index": None
                }
            }
        }
@tool
def check_author_name_format(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    检查作者姓名格式是否符合用户的具体要求。

    输入 state 包含：
        - requirement: 用户的具体格式要求（如"姓全大写，名首字母大写"）
        - content_to_check: 待检查的作者姓名文本

    Returns:
        dict: 检查结果，格式与其他检查工具一致
    """
    requirement = state.get("requirement", "").strip()
    content = state.get("content_to_check", "").strip()

    if not content:
        return {
            "status": "failed",
            "type": "check",
            "data": {
                "result": False,
                "check_name": "作者姓名格式检查",
                "message": "缺少待检查的作者姓名内容",
                "severity": "error",
                "revision_comment": {
                    "author": "格式检查器",
                    "text": "缺少作者姓名信息，请补充完整",
                    "paragraph_index": None,
                    "run_index": None
                }
            }
        }

    if not requirement:
        # 默认的英文作者姓名格式要求
        requirement = "英文作者姓名格式：姓全大写，名首字母大写，双名中间加连字符，姓与名之间用空格分隔。示例：ZHANG Ying, WANG Xi-lian"

    # 专门针对作者姓名格式检查的提示词
    prompt_template = """
请检查以下作者姓名格式是否符合要求：

【格式要求】
{requirement}

【待检查的作者姓名】
{content}

请判断姓名格式是否符合要求。如果不符合，请简要说明问题。
只返回：符合 或 不符合+原因
"""

    try:
        prompt = prompt_template.format(
            requirement=requirement,
            content=content
        )
        llm = zhipu_llm(temperature=0.1)
        response = llm.invoke(prompt)
        raw_output = response.content.strip()

        # 解析模型响应
        if "符合" in raw_output and "不符合" not in raw_output:
            return {
                "status": "success",
                "type": "check",
                "data": {
                    "result": True,
                    "check_name": "作者姓名格式检查",
                    "message": f"作者姓名格式符合要求：{requirement}",
                    "severity": "info"
                }
            }
        else:
            # 提取不符合的原因
            if "不符合" in raw_output:
                reason = raw_output.split("不符合")[1].strip()
            else:
                reason = "姓名格式不符合要求"

            # 限制原因长度
            reason = reason[:40] + "..." if len(reason) > 40 else reason

            return {
                "status": "failed",
                "type": "check",
                "data": {
                    "result": False,
                    "check_name": "作者姓名格式检查",
                    "message": f"作者姓名格式不符合要求：{reason}",
                    "severity": "error",
                    "revision_comment": {
                        "author": "格式检查器",
                        "text": f"作者姓名格式问题：{reason}",
                        "paragraph_index": None,
                        "run_index": None
                    }
                }
            }

    except Exception as e:
        return {
            "status": "failed",
            "type": "check",
            "data": {
                "result": False,
                "check_name": "作者姓名格式检查",
                "message": f"检查过程中发生错误: {str(e)}",
                "severity": "error",
                "revision_comment": {
                    "author": "格式检查器",
                    "text": "姓名格式检查异常，请手动验证",
                    "paragraph_index": None,
                    "run_index": None
                }
            }
        }


# 执行类工具
@tool
def set_font_name(font_name: str) -> Dict[str, Any]:
    """
    设置当前段落或文本的字体名称。

    Args:
        font_name (str):
            字体名称，必须是系统支持的中文字体。
            常见取值：'宋体'、'黑体'、'楷体'、'仿宋'、'微软雅黑'、'Times New Roman' 等。
            必需参数。

    Returns:
        dict: 指令字典，包含操作类型和样式设置。
    """
    return {
        "status":"success",
        "action": "set_font",
        "data": {
            "styles": {"font_name": font_name}
        }
    }
@tool
def set_font_size(pt: float) -> Dict[str, Any]:
    """
    设置当前字体的大小（以磅 Pt 为单位）。

    Args:
        pt (float):
            字号大小，单位为磅（Pt）。
            常见中文排版对照：
                - 三号 ≈ 16pt
                - 小四 ≈ 12pt
                - 五号 ≈ 10.5pt
                - 四号 ≈ 14pt
            必需参数，建议使用 8.0 ~ 72.0 范围内的数值。

    Returns:
        dict: 指令字典，包含操作类型和字号设置。
    """
    return {
        "status": "success",
        "action": "set_font",
        "data": {
            "styles": {"font_size": pt}
        }
    }
@tool
def set_font_bold(bold: bool = True) -> Dict[str, Any]:
    """
    设置字体是否加粗。

    Args:
        bold (bool):
            是否加粗。
            - True：加粗（默认）
            - False：取消加粗
            可选参数，默认为 True。

    Returns:
        dict: 指令字典，包含加粗设置。
    """
    return {
        "status": "success",
        "action": "set_font",
        "data": {
            "styles": {"bold": bold}
        }
    }
@tool
def set_font_italic(italic: bool = True) -> Dict[str, Any]:
    """
    设置字体是否为斜体。

    Args:
        italic (bool):
            是否设置为斜体。
            - True：斜体（默认）
            - False：取消斜体
            可选参数，默认为 True。

    Returns:
        dict: 指令字典，包含斜体设置。
    """
    return {
        "status": "success",
        "action": "set_font",
        "data": {
            "styles": {"italic": italic}
        }
    }
@tool
def set_paragraph_align(align: Literal["left", "center", "right", "justify"]) -> Dict[str, Any]:
    """
    设置段落对齐方式。

    Args:
        align (str):
            对齐方式，枚举值，必须为以下之一：
            - 'left'     -> 左对齐
            - 'center'   -> 居中对齐
            - 'right'    -> 右对齐
            - 'justify'  -> 两端对齐（推荐用于正文）
            必需参数。

    Returns:
        dict: 指令字典，包含段落对齐设置。
    """
    align_map = {
        "left": "左对齐",
        "center": "居中",
        "right": "右对齐",
        "justify": "两端对齐"
    }
    zh = align_map.get(align, "未知")
    return {
        "status": "success",
        "action": "set_paragraph",
        "data": {
            "styles": {"align": align}
        }
    }
@tool
def set_line_spacing(multiple: float) -> Dict[str, Any]:
    """
    设置段落行距（倍数行距）。

    Args:
        multiple (float):
            行距倍数，如 1.0、1.5、2.0。
            常见取值：
                - 1.5 倍：学术论文常用
                - 1.0 倍：单倍行距
                - 2.0 倍：双倍行距
            必需参数，建议取值范围：1.0 ~ 3.0。

    Returns:
        dict: 指令字典，包含行距设置。
    """
    return {
        "status": "success",
        "action": "set_paragraph",
        "data": {
            "styles": {"line_spacing": multiple}
        }
    }
@tool
def set_paragraph_indent(first_line: Optional[float] = None,hanging: Optional[float] = None) -> Dict[str, Any]:
    """
    设置段落缩进（支持首行缩进和悬挂缩进）。

    Args:
        first_line (float, optional):
            首行缩进字符数（正数），例如 2.0 表示缩进两个汉字位置。
        hanging (float, optional):
            悬挂缩进字符数（正数），常用于参考文献列表。

        注意：first_line 和 hanging 不应同时设置。

    Returns:
        dict: 指令字典，包含缩进设置。
    """
    indent_info = {}
    if first_line is not None:
        indent_info["first_line"] = first_line
    if hanging is not None:
        indent_info["hanging"] = hanging
    return {
        "status": "success",
        "action": "set_paragraph",
        "data": {
            "styles": {"indent": indent_info}
        }
    }
