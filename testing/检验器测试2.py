import json
from typing import Dict, Any, List
from tools.utils import zhipu_llm
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate


def validator_node_test(json_file_path: str):
    """
    测试版本的验证器节点，从JSON文件读取执行结果进行验证
    """
    system_messages = [
        SystemMessage(content="<-- 进入 08 检验器节点（测试版） -->")
    ]

    llm = zhipu_llm(model="glm-4.5-air", temperature=0.3, timeout=240.0)


    prompt_template = """
请对比用户要求和实际执行结果，给出整体判断：

【用户要求与执行结果对比】
{task_and_result}

请返回JSON格式：
{{
  "overall_status": "success|partial_success|failed",
  "verification_result": [
    {{
      "section": "章节名称",
      "subsection": "子章节名称",
      "status": "success|failed",
      "reason": "简要说明原因（如果是失败）"
    }}
  ],
  "summary": "整体评估摘要"
}}
"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的格式验证器，负责对比用户要求和实际执行结果。"),
        ("human", prompt_template)
    ])


    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
    except Exception as e:
        return {
            "error": f"读取JSON文件失败: {str(e)}",
            "messages": [SystemMessage(content=f"❌ 文件读取错误: {str(e)}")]
        }

    # 收集所有需要验证的任务
    verification_tasks = []

    state1 = {
        "agent_mission": [
            {
                "section": "首页",
                "subsection": "论文题目",
                "content": "基于《金匮要略》的多粒度知识表示模型构建研究",
                "para_index": 0,
                "request": [
                    {
                        "字体": "宋体"
                    },
                    {
                        "字号": "三号"
                    },
                    {
                        "加粗": "是"
                    },
                    {
                        "对齐": "居中"
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "作者姓名",
                "content": "王世文  赵泽儒*  邢建斌",
                "para_index": 1,
                "request": [
                    {
                        "字体": "宋体"
                    },
                    {
                        "字号": "小四"
                    },
                    {
                        "对齐": "居中"
                    },
                    {
                        "行距": "1.5倍行距"
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "作者单位",
                "content": "（天津师范大学 管理学院，天津  300387）",
                "para_index": 2,
                "request": [
                    {
                        "字体": "宋体"
                    },
                    {
                        "字号": "五号"
                    },
                    {
                        "对齐": "居中"
                    },
                    {
                        "行距": "1.5倍行距"
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "摘要",
                "content": "摘要：[目的] 本文基于多粒度层级划分提出多粒度的知识表示框架与模型，以提升中医古籍知识挖掘与利用效率。[方法] 本文首先通过对《金匮要略》的分析与归纳，提出从知识内容角度出发的多粒度层级划分结构。然后，据此构建出中医古籍多粒度知识表示框架，并给出多粒度知识表示模型，并以《金匮要略》和《温病条辨》中的知识内容进行了模型展示与验证。[结果] 对多粒度知识表示模型的应用，展示出模型的普适性和科学性，体现出模型在中医古籍领域中的可用性和有效性，有效支持中医古籍知识表示与组织。[结论] 多粒度知识表示模型为中医古籍知识挖掘与组织提供了可行方案，具有理论与实践价值。",
                "para_index": 3,
                "request": [
                    {
                        "字体": "宋体"
                    },
                    {
                        "字号": "小四"
                    },
                    {
                        "行距": "1.5倍行距"
                    },
                    {
                        "格式": "【目的/意义】……【方法/过程】……【结果/结论】……【创新/局限】"
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "关键词",
                "content": "关键词：中医古籍；知识表示；多粒度；知识元；知识表示模型",
                "para_index": 4,
                "request": [
                    {
                        "字体": "宋体"
                    },
                    {
                        "字号": "五号"
                    },
                    {
                        "行距": "1.5倍"
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "中图分类号",
                "content": "分类号：G254",
                "para_index": 5,
                "request": [
                    {
                        "字体": "宋体"
                    },
                    {
                        "字号": "五号"
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "英文题目",
                "content": "Construction of a Multi-Granularity Knowledge Representation Model Based on Synopsis of Golden Chamber",
                "para_index": 7,
                "request": [
                    {
                        "字体": "Times New Roman"
                    },
                    {
                        "字号": "三号"
                    },
                    {
                        "加粗": "是"
                    },
                    {
                        "对齐": "居中"
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "英文作者姓名",
                "content": "WANG Shi-wen  ZHAO Ze-ru*",
                "para_index": 8,
                "request": [
                    {
                        "字体": "Times New Roman"
                    },
                    {
                        "字号": "小四"
                    },
                    {
                        "对齐": "居中"
                    },
                    {
                        "行距": "1.5倍行距"
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "英文作者单位",
                "content": "(College of Management‌, Tianjin Normal University, Tianjin, 300387)",
                "para_index": 9,
                "request": [
                    {
                        "字体": "Times New Roman"
                    },
                    {
                        "字号": "五号"
                    },
                    {
                        "对齐": "居中"
                    },
                    {
                        "行距": "1.5倍行距"
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "英文摘要",
                "content": "Abstract：[Objective] This paper proposes a multi-granularity knowledge representation framework and model based on multi-granularity hierarchical division to enhance the efficiency of knowledge mining and utilization in ancient Chinese medical literature.[Methods] This article first proposes a multi granularity hierarchical structure from the perspective of knowledge content by analyzing and summarizing the \"quot;Synopsis of the Golden Chamber\"quot;. Then, based on this, a multi granularity knowledge representation framework for traditional Chinese medicine ancient books was constructed, and a multi granularity knowledge representation model was proposed. The model was demonstrated and validated using the knowledge content from \"quot;Synopsis of Golden Chamber\"quot; and \"quot;Wenbing Tiaobian\"quot;.[Results] The application of multi granularity knowledge representation models demonstrates the universality and scientificity of the models, reflecting their usability and effectiveness in the field of traditional Chinese medicine ancient books, and effectively supporting the representation and organization of traditional Chinese medicine ancient book knowledge.[Conclusions] The multi-granularity knowledge representation model provides a feasible solution for knowledge mining and organization in ancient Chinese medical literature, with both theoretical and practical significance.",
                "para_index": 10,
                "request": [
                    {
                        "字体": "Times New Roman"
                    },
                    {
                        "字号": "小四"
                    },
                    {
                        "行距": "1.5倍行距"
                    },
                    {
                        "格式": "【目的/意义】……【方法/过程】……【结果/结论】……【创新/局限】"
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "英文关键词",
                "content": "Keywords： TCM ancient literature; knowledge representation; multi-granularity; knowledge element; Description model of knowledge",
                "para_index": 11,
                "request": [
                    {
                        "字体": "Times New Roman"
                    },
                    {
                        "字号": "五号"
                    },
                    {
                        "行距": "1.5倍"
                    }
                ]
            },
            {
                "section": "其他排版要求",
                "subsection": "未在文档中出现的部分",
                "request": [
                    {
                        "subsection": "页面布局",
                        "missing_request": []
                    },
                    {
                        "subsection": "副题目",
                        "missing_request": [
                            {
                                "对齐": "右对齐"
                            }
                        ]
                    },
                    {
                        "subsection": "正文段落",
                        "missing_request": [
                            {
                                "字体": "宋体"
                            },
                            {
                                "字号": "小四"
                            },
                            {
                                "行距": "1.5倍"
                            },
                            {
                                "段落格式": "首行缩进2字符"
                            }
                        ]
                    },
                    {
                        "subsection": "一级标题",
                        "missing_request": [
                            {
                                "字体": "黑体"
                            },
                            {
                                "字号": "三号"
                            },
                            {
                                "加粗": "是"
                            },
                            {
                                "对齐": "居中"
                            },
                            {
                                "段前段后": "各12pt"
                            }
                        ]
                    },
                    {
                        "subsection": "二级标题",
                        "missing_request": [
                            {
                                "字体": "黑体"
                            },
                            {
                                "字号": "四号"
                            },
                            {
                                "加粗": "是"
                            },
                            {
                                "对齐": "左对齐"
                            },
                            {
                                "段前段后": "各6pt"
                            }
                        ]
                    },
                    {
                        "subsection": "三级标题",
                        "missing_request": [
                            {
                                "字体": "楷体"
                            },
                            {
                                "字号": "小四"
                            },
                            {
                                "加粗": "是"
                            },
                            {
                                "对齐": "左对齐"
                            }
                        ]
                    },
                    {
                        "subsection": "图表",
                        "missing_request": []
                    },
                    {
                        "subsection": "公式",
                        "missing_request": []
                    },
                    {
                        "subsection": "算法",
                        "missing_request": []
                    },
                    {
                        "subsection": "代码片段",
                        "missing_request": []
                    },
                    {
                        "subsection": "文献列表",
                        "missing_request": []
                    },
                    {
                        "subsection": "作者简介",
                        "missing_request": []
                    },
                    {
                        "subsection": "作者贡献声明",
                        "missing_request": []
                    },
                    {
                        "subsection": "课题或基金项目",
                        "missing_request": []
                    }
                ]
            }
        ]
    }
    state2 = state_data.get("cover")
    if state2 and state1:
        missions = state1.get("agent_mission", [])
        results = state2.get("agent_result", {}).get("layout_result", [])

        # 创建执行结果映射
        exec_map = {}
        for result in results:
            key = (result.get("section"), result.get("subsection"))
            exec_map[key] = result

        for mission in missions:
            # 跳过系统默认的请求
            if isinstance(mission.get("request"), dict) and mission.get("request", {}).get(
                    "source") == "system_default":
                continue

            sec = mission.get("section")
            subsec = mission.get("subsection")
            content = mission.get("content", "")

            # 获取执行结果
            exec_result = exec_map.get((sec, subsec), {})

            verification_tasks.append({
                "section": sec,
                "subsection": subsec,
                "content": content,
                "request": mission.get("request", []),
                "execution_result": exec_result
            })

    # 如果没有需要验证的任务，直接返回成功
    if not verification_tasks:
        return {
            "verification_status": "ok",
            "should_terminate": True,
            "verification_result": [],
            "messages": system_messages + [
                AIMessage(content="✅ 无需要验证的任务，检验通过")
            ],
        }

    try:
        # 调用LLM进行整体验证
        response = llm.invoke(
            prompt.format(
                task_and_result=json.dumps(verification_tasks, ensure_ascii=False, indent=2)
            )
        )

        content = response.content.strip()
        # 清理JSON格式
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()

        result_json = json.loads(content)

        # 提取验证结果
        overall_status = result_json.get("overall_status", "failed")
        verification_results = result_json.get("verification_result", [])
        summary = result_json.get("summary", "")

        # 根据整体状态决定是否终止
        if overall_status == "success":
            verification_status = "ok"
            should_terminate = True
        elif overall_status == "partial_success":
            verification_status = "again"
            should_terminate = False
        else:  # failed
            verification_status = "again"
            should_terminate = False

        system_messages.append(
            SystemMessage(content=f"📊 整体验证状态: {overall_status}, 总结: {summary}")
        )

        # 打印详细结果
        print(f"整体状态: {overall_status}")
        print(f"总结: {summary}")
        print("\n详细验证结果:")
        for result in verification_results:
            status_icon = "✅" if result.get("status") == "success" else "❌"
            print(f"{status_icon} {result.get('section')} - {result.get('subsection')}: {result.get('reason', '')}")

        return {
            "verification_status": verification_status,
            "should_terminate": should_terminate,
            "verification_result": verification_results,
            "overall_summary": summary,
            "messages": system_messages + [
                AIMessage(content=f"✅ 检验器校验结束，总体状态: {overall_status}")
            ],
        }

    except Exception as e:
        # LLM调用失败，默认所有任务都需要重试
        error_message = f"验证过程中发生错误: {str(e)}"
        system_messages.append(SystemMessage(content=f"❌ {error_message}"))

        # 创建默认的失败结果
        default_results = []
        for task in verification_tasks:
            default_results.append({
                "section": task["section"],
                "subsection": task["subsection"],
                "status": "failed",
                "reason": error_message
            })

        return {
            "verification_status": "again",
            "should_terminate": False,
            "verification_result": default_results,
            "overall_summary": "验证过程发生错误，需要重新尝试",
            "messages": system_messages + [
                AIMessage(content="❌ 验证过程出错，需要重新处理")
            ],
        }


# 使用示例
if __name__ == "__main__":
    # 替换为您的JSON文件路径
    json_file_path = r"C:\Users\Administrator\Desktop\cover执行结果.json"

    # 运行测试
    result = validator_node_test(json_file_path)

    # === 预处理 result，将不可序列化的对象转为字典或字符串 ===
    def serialize_message(msg):
        if isinstance(msg, (SystemMessage, AIMessage)):
            return {
                "type": msg.type,
                "content": msg.content
            }
        else:
            return str(msg)  # 兜底转为字符串

    # 复制 result 并处理 messages
    serializable_result = result.copy()
    if "messages" in serializable_result:
        serializable_result["messages"] = [
            serialize_message(msg) for msg in serializable_result["messages"]
        ]

    # 输出结果
    print("\n最终结果:")
    print(json.dumps(serializable_result, ensure_ascii=False, indent=2))