from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import json
state = {"cover":{
    "agent_mission": [
        {
            "section": "首页",
            "subsection": "论文题目",
            "content": "基于《金匮要略》的多粒度知识表示模型构建研究",
            "para_index": 0,
            "request": [
                {"字体": "宋体"},
                {"字号": "三号"},
                {"加粗": "是"},
                {"对齐": "居中"}
            ]
        },
        {
            "section": "首页",
            "subsection": "作者姓名",
            "content": "王世文  赵泽儒*  邢建斌",
            "para_index": 1,
            "request": [
                {"字体": "宋体"},
                {"字号": "小四"},
                {"对齐": "居中"},
                {"行距": "1.5倍"}
            ]
        },
        {
            "section": "首页",
            "subsection": "作者单位",
            "content": "（天津师范大学 管理学院，天津  300387）",
            "para_index": 2,
            "request": [
                {"字体": "宋体"},
                {"字号": "五号"},
                {"对齐": "居中"},
                {"行距": "1.5倍"}
            ]
        },
        {
            "section": "首页",
            "subsection": "摘要",
            "content": "摘要：[目的] 本文基于多粒度层级划分提出多粒度的知识表示框架与模型，以提升中医古籍知识挖掘与利用效率。[方法] 本文首先通过对《金匮要略》的分析与归纳，提出从知识内容角度出发的多粒度层级划分结构。然后，据此构建出中医古籍多粒度知识表示框架，并给出多粒度知识表示模型，并以《金匮要略》和《温病条辨》中的知识内容进行了模型展示与验证。[结果] 对多粒度知识表示模型的应用，展示出模型的普适性和科学性，体现出模型在中医古籍领域中的可用性和有效性，有效支持中医古籍知识表示与组织。[结论] 多粒度知识表示模型为中医古籍知识挖掘与组织提供了可行方案，具有理论与实践价值。",
            "para_index": 3,
            "request": [
                {"字体": "宋体"},
                {"字号": "小四"},
                {"行距": "1.5倍"}
            ]
        },
        {
            "section": "首页",
            "subsection": "关键词",
            "content": "关键词：中医古籍；知识表示；多粒度；知识元；知识表示模型",
            "para_index": 4,
            "request": [
                {"数量": "5个及以上"},
                {"字体": "无"},
                {"字号": "无"},
                {"对齐": "无"}
            ]
        },
        {
            "section": "首页",
            "subsection": "中图分类号",
            "content": "分类号：G254",
            "para_index": 5,
            "request": {
                "items": [
                    {"字体": "宋体"},
                    {"字号": "五号"}
                ],
                "source": "system_default"
            }
        },
        {
            "section": "首页",
            "subsection": "英文题目",
            "content": "Construction of a Multi-Granularity Knowledge Representation Model Based on Synopsis of Golden Chamber",
            "para_index": 7,
            "request": [
                {"字体": "Times New Roman"},
                {"字号": "三号"},
                {"加粗": "无"},
                {"对齐": "居中"}
            ]
        },
        {
            "section": "首页",
            "subsection": "英文作者姓名",
            "content": "WANG Shi-wen  ZHAO Ze-ru*",
            "para_index": 8,
            "request": [
                {"格式": "姓前名后，中间为空格，姓氏的全部字母均大写，名字的首字母大写，双名中间加连字符"},
                {"字体": "Times New Roman"},
                {"字号": "小四"},
                {"对齐": "居中"}
            ]
        },
        {
            "section": "首页",
            "subsection": "英文作者单位",
            "content": "(College of Management, Tianjin Normal University, Tianjin, 300387)",
            "para_index": 9,
            "request": [
                {"格式": "单位全称及具体部门、所在省市及邮政编码"},
                {"字体": "Times New Roman"},
                {"字号": "五号"},
                {"对齐": "居中"}
            ]
        },
        {
            "section": "首页",
            "subsection": "英文摘要",
            "content": "Abstract：[Objective] This paper proposes a multi-granularity knowledge representation framework and model based on multi-granularity hierarchical division to enhance the efficiency of knowledge mining and utilization in ancient Chinese medical literature.[Methods] This article first proposes a multi granularity hierarchical structure from the perspective of knowledge content by analyzing and summarizing the \"Synopsis of the Golden Chamber\". Then, based on this, a multi granularity knowledge representation framework for traditional Chinese medicine ancient books was constructed, and a multi granularity knowledge representation model was proposed. The model was demonstrated and validated using the knowledge content from \"Synopsis of Golden Chamber\" and \"Wenbing Tiaobian\".[Results] The application of multi granularity knowledge representation models demonstrates the universality and scientificity of the models, reflecting their usability and effectiveness in the field of traditional Chinese medicine ancient books, and effectively supporting the representation and organization of traditional Chinese medicine ancient book knowledge.[Conclusions] The multi-granularity knowledge representation model provides a feasible solution for knowledge mining and organization in ancient Chinese medical literature, with both theoretical and practical significance.",
            "para_index": 10,
            "request": [
                {"字体": "Times New Roman"},
                {"字号": "小四"},
                {"行距": "1.5倍"}
            ]
        },
        {
            "section": "首页",
            "subsection": "英文关键词",
            "content": "Keywords： TCM ancient literature; knowledge representation; multi-granularity; knowledge element; Description model of knowledge",
            "para_index": 11,
            "request": [
                {"数量": "与中文关键词相对应"},
                {"字体": "Times New Roman"},
                {"字号": "无"},
                {"对齐": "无"}
            ]
        }
    ],
    "agent_result": {
        "status": "success",
        "layout_result": [
            {
                "section": "首页",
                "subsection": "论文题目",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "set_font_name",
                        "args": {"font_name": "宋体"},
                        "id": "call_-8407379513614623967",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_font_size",
                        "args": {"pt": 16},
                        "id": "call_-8407379513614623966",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_font_bold",
                        "args": {"bold": True},
                        "id": "call_-8407379513614623965",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_paragraph_align",
                        "args": {"align": "center"},
                        "id": "call_-8407379513614623964",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407379513614623967",
                        "tool_name": "set_font_name",
                        "args": {"font_name": "宋体"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_name": "宋体"}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407379513614623966",
                        "tool_name": "set_font_size",
                        "args": {"pt": 16},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_size": 16.0}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407379513614623965",
                        "tool_name": "set_font_bold",
                        "args": {"bold": True},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"bold": True}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407379513614623964",
                        "tool_name": "set_paragraph_align",
                        "args": {"align": "center"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_paragraph",
                                "styles": {"align": "center"}
                            }
                        }
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "作者姓名",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "set_font_name",
                        "args": {"font_name": "宋体"},
                        "id": "call_-8407406829607674094",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_font_size",
                        "args": {"pt": 12},
                        "id": "call_-8407406829607674093",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_paragraph_align",
                        "args": {"align": "center"},
                        "id": "call_-8407406829607674092",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_line_spacing",
                        "args": {"multiple": 1.5},
                        "id": "call_-8407406829607674091",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407406829607674094",
                        "tool_name": "set_font_name",
                        "args": {"font_name": "宋体"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_name": "宋体"}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407406829607674093",
                        "tool_name": "set_font_size",
                        "args": {"pt": 12},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_size": 12.0}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407406829607674092",
                        "tool_name": "set_paragraph_align",
                        "args": {"align": "center"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_paragraph",
                                "styles": {"align": "center"}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407406829607674091",
                        "tool_name": "set_line_spacing",
                        "args": {"multiple": 1.5},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_paragraph",
                                "styles": {"line_spacing": 1.5}
                            }
                        }
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "作者单位",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "set_font_name",
                        "args": {"font_name": "宋体"},
                        "id": "call_-8407379651053642624",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_font_size",
                        "args": {"pt": 10.5},
                        "id": "call_-8407379651053642623",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_paragraph_align",
                        "args": {"align": "center"},
                        "id": "call_-8407379651053642622",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_line_spacing",
                        "args": {"multiple": 1.5},
                        "id": "call_-8407379651053642621",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407379651053642624",
                        "tool_name": "set_font_name",
                        "args": {"font_name": "宋体"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_name": "宋体"}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407379651053642623",
                        "tool_name": "set_font_size",
                        "args": {"pt": 10.5},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_size": 10.5}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407379651053642622",
                        "tool_name": "set_paragraph_align",
                        "args": {"align": "center"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_paragraph",
                                "styles": {"align": "center"}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407379651053642621",
                        "tool_name": "set_line_spacing",
                        "args": {"multiple": 1.5},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_paragraph",
                                "styles": {"line_spacing": 1.5}
                            }
                        }
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "摘要",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "set_font_name",
                        "args": {"font_name": "宋体"},
                        "id": "call_-8407380544407086238",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_font_size",
                        "args": {"pt": 12},
                        "id": "call_-8407380544407086237",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_line_spacing",
                        "args": {"multiple": 1.5},
                        "id": "call_-8407380544407086236",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407380544407086238",
                        "tool_name": "set_font_name",
                        "args": {"font_name": "宋体"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_name": "宋体"}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407380544407086237",
                        "tool_name": "set_font_size",
                        "args": {"pt": 12},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_size": 12.0}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407380544407086236",
                        "tool_name": "set_line_spacing",
                        "args": {"multiple": 1.5},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_paragraph",
                                "styles": {"line_spacing": 1.5}
                            }
                        }
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "关键词",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "check_keyword_count",
                        "args": {
                            "keywords": "中医古籍；知识表示；多粒度；知识元；知识表示模型",
                            "min_count": 5
                        },
                        "id": "call_-8407340858906601526",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407340858906601526",
                        "tool_name": "check_keyword_count",
                        "args": {
                            "keywords": "中医古籍；知识表示；多粒度；知识元；知识表示模型",
                            "min_count": 5
                        },
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "result": True,
                                "message": "关键词数量合规：5 个",
                                "severity": "info",
                                "details": {
                                    "count": 5,
                                    "keywords_list": [
                                        "中医古籍",
                                        "知识表示",
                                        "多粒度",
                                        "知识元",
                                        "知识表示模型"
                                    ]
                                }
                            }
                        }
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "中图分类号",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "set_font_name",
                        "args": {"font_name": "宋体"},
                        "id": "call_-8407344123081910267",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_font_size",
                        "args": {"pt": 10.5},
                        "id": "call_-8407344123081910266",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407344123081910267",
                        "tool_name": "set_font_name",
                        "args": {"font_name": "宋体"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_name": "宋体"}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407344123081910266",
                        "tool_name": "set_font_size",
                        "args": {"pt": 10.5},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_size": 10.5}
                            }
                        }
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "英文题目",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "set_font_name",
                        "args": {"font_name": "Times New Roman"},
                        "id": "call_-8407381403400643792",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_font_size",
                        "args": {"pt": 16},
                        "id": "call_-8407381403400643791",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_font_bold",
                        "args": {"bold": False},
                        "id": "call_-8407381403400643790",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_paragraph_align",
                        "args": {"align": "center"},
                        "id": "call_-8407381403400643789",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407381403400643792",
                        "tool_name": "set_font_name",
                        "args": {"font_name": "Times New Roman"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_name": "Times New Roman"}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407381403400643791",
                        "tool_name": "set_font_size",
                        "args": {"pt": 16},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_size": 16.0}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407381403400643790",
                        "tool_name": "set_font_bold",
                        "args": {"bold": False},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"bold": False}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407381403400643789",
                        "tool_name": "set_paragraph_align",
                        "args": {"align": "center"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_paragraph",
                                "styles": {"align": "center"}
                            }
                        }
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "英文作者姓名",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "check_author_affiliation_by_llm",
                        "args": {
                            "state": {
                                "requirement": "姓前名后，中间为空格，姓氏的全部字母均大写，名字的首字母大写，双名中间加连字符",
                                "content_to_check": "WANG Shi-wen  ZHAO Ze-ru*"
                            }
                        },
                        "id": "call_-8407336907536517223",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407336907536517223",
                        "tool_name": "check_author_affiliation_by_llm",
                        "args": {
                            "state": {
                                "requirement": "姓前名后，中间为空格，姓氏的全部字母均大写，名字的首字母大写，双名中间加连字符",
                                "content_to_check": "WANG Shi-wen  ZHAO Ze-ru*"
                            }
                        },
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "result": False,
                                "check_name": "检查作者和作者单位格式",
                                "message": "格式不符合，发现 1 个问题",
                                "severity": "error",
                                "details": {
                                    "issues": ["名字部分包含非法字符星号(*)，不符合格式要求（名字应仅包含字母，首字母大写，双名中间加连字符）"],
                                    "raw_model_output": '{\n  "compliant": false,\n  "issues": [\n    "名字部分包含非法字符星号(*)，不符合格式要求（名字应仅包含字母，首字母大写，双名中间加连字符）"\n  ]\n}'
                                }
                            }
                        }
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "英文作者单位",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "set_font_name",
                        "args": {"font_name": "Times New Roman"},
                        "id": "call_-8407379238736610244",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_font_size",
                        "args": {"pt": 10.5},
                        "id": "call_-8407379238736610243",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_paragraph_align",
                        "args": {"align": "center"},
                        "id": "call_-8407379238736610242",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407379238736610244",
                        "tool_name": "set_font_name",
                        "args": {"font_name": "Times New Roman"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_name": "Times New Roman"}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407379238736610243",
                        "tool_name": "set_font_size",
                        "args": {"pt": 10.5},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_size": 10.5}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407379238736610242",
                        "tool_name": "set_paragraph_align",
                        "args": {"align": "center"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_paragraph",
                                "styles": {"align": "center"}
                            }
                        }
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "英文摘要",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "set_font_name",
                        "args": {"font_name": "Times New Roman"},
                        "id": "call_-8407356767466538107",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_font_size",
                        "args": {"pt": 12},
                        "id": "call_-8407356767466538106",
                        "type": "tool_call"
                    },
                    {
                        "name": "set_line_spacing",
                        "args": {"multiple": 1.5},
                        "id": "call_-8407356767466538105",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407356767466538107",
                        "tool_name": "set_font_name",
                        "args": {"font_name": "Times New Roman"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_name": "Times New Roman"}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407356767466538106",
                        "tool_name": "set_font_size",
                        "args": {"pt": 12},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_size": 12.0}
                            }
                        }
                    },
                    {
                        "tool_call_id": "call_-8407356767466538105",
                        "tool_name": "set_line_spacing",
                        "args": {"multiple": 1.5},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_paragraph",
                                "styles": {"line_spacing": 1.5}
                            }
                        }
                    }
                ]
            },
            {
                "section": "首页",
                "subsection": "英文关键词",
                "status": "success",
                "raw_model_response": "",
                "tool_calls": [
                    {
                        "name": "set_font_name",
                        "args": {"font_name": "Times New Roman"},
                        "id": "call_-8407356423869113609",
                        "type": "tool_call"
                    }
                ],
                "tool_execution_results": [
                    {
                        "tool_call_id": "call_-8407356423869113609",
                        "tool_name": "set_font_name",
                        "args": {"font_name": "Times New Roman"},
                        "execution_result": {
                            "status": "success",
                            "result": {
                                "action": "set_font",
                                "styles": {"font_name": "Times New Roman"}
                            }
                        }
                    }
                ]
            }
        ]
    }
}
}
validator_system_prompt = """
你是一个严格的排版任务审查专家。请根据用户的原始请求，审查 AI 是否正确执行了每一个任务。

输入格式：
[
  {{
    "agent_name": "author",
    "original_request": {{ "section": "摘要", "subsection": "字体", "request": [{{"字体": "宋体"}}] }},
    "execution_result": {{ "section": "摘要", "subsection": "字体", "result": "宋体" }}
  }},
  ...
]

请返回 JSON 格式：
{{
  "verification_result": [
    {{
      "agent_name": "author",
      "section": "摘要",
      "subsection": "字体",
      "request": {{"字体": "宋体"}},
      "status": "success|failed",
      "reason": "解释原因"
    }}
  ]
}}
"""
ZHIPUAI_API_KEY ="f4909101a9ae4b11b9360187bb23e4b5.jhAhTcvXbY4gUWUx"
def zhipu_llm(model: str = 'glm-4.5-air',api_key: str = ZHIPUAI_API_KEY,thinking: str = 'enabled',stream: bool = True,temperature: float = 0.7,timeout: float = 30.0,**kwargs):
    return ChatZhipuAI(
        api_key=api_key,
        model=model,
        thinking={
            "type": thinking,
        },
        stream=stream,
        temperature=temperature,
        timeout=timeout,
        **kwargs
    )

llm = zhipu_llm(model="glm-4.5-air", temperature=0.1, timeout=120.0)
system_prompt = validator_system_prompt

# 构建 prompt：支持批量任务校验
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        (
            "human",
            "请审查以下多个任务的执行情况，并对每一项返回校验结果：\n{task_and_result_batch}\n"
            "要求返回一个 JSON 列表，每个元素包含 section、subsection、status、reason。",
        ),
    ]
)

# ===== 收集所有待校验任务 =====
all_tasks_for_validation = []
# agents = ["author", "chart", "cover", "fund", "reference", "text", "other"]
agents = ["cover"]

print("🔍 [DEBUG] 开始收集各 agent 的待校验任务...")

for agent_name in agents:
    agent_state = state.get(agent_name)
    if not agent_state:
        print(f"  ⚠️  agent '{agent_name}' 不存在于 state 中，跳过")
        continue

    missions = agent_state.get("agent_mission", [])
    results = agent_state.get("agent_result", {}).get("layout_result", [])
    print(f"  ✅ agent '{agent_name}': missions={len(missions)}, results={len(results)}")

    exec_map = {(item["section"], item["subsection"]): item for item in results}

    for mission in missions:
        if isinstance(mission.get("request"), dict) and mission["request"].get("source") == "system_default":
            continue
        sec = mission["section"]
        subsec = mission["subsection"]
        # 🔧 安全处理 request 字段
        raw_request = mission.get("request", [])
        if isinstance(raw_request, list):
            # 如果是列表，尝试合并字典
            request_dict = {}
            for req in raw_request:
                if isinstance(req, dict):
                    request_dict.update(req)
                elif isinstance(req, str):
                    # 如果列表里是字符串，可以加到 description 字段
                    request_dict.setdefault("description", []).append(req)
            request = request_dict
        elif isinstance(raw_request, str):
            # 如果是字符串，包装成字典
            request = {"description": raw_request}
        elif isinstance(raw_request, dict):
            # 如果本身就是字典
            request = raw_request.copy()
        else:
            request = {"error": "unknown request format"}

        exec_result = exec_map.get((sec, subsec))
        if not exec_result:
            all_tasks_for_validation.append({
                "agent_name": agent_name,
                "section": sec,
                "subsection": subsec,
                "request": request,
                "original_request": mission,
                "execution_result": None,
                "error": f"[{agent_name}] 该任务未被执行（无执行记录）"
            })
            print(f"    🔻 未执行任务: ({sec}/{subsec})")
        else:
            all_tasks_for_validation.append({
                "agent_name": agent_name,
                "section": sec,
                "subsection": subsec,
                "request": request,
                "original_request": mission,
                "execution_result": exec_result
            })
            print(f"    ✅ 已执行任务: ({sec}/{subsec})")

print(f"📊 [DEBUG] 共收集到 {len(all_tasks_for_validation)} 个待校验任务")

# ===== 如果没有任务，直接返回 =====
if not all_tasks_for_validation:
    print(">>>>>>   无任何任务需要校验")
    return1 = {
        "verification_status": "ok",
        "should_terminate": True,
        "verification_success_result": [],
        "verification_failed_result": [],
        "messages": [AIMessage(content="✅ 检验器校验结束，无任务需要校验。")],
    }
    print("🔚 [RETURN] 无任务，直接返回:", return1)
    # return return1  # 取消注释正式使用
else:
    print("📝 [DEBUG] 准备发送给 LLM 的任务列表示例:")
    print(json.dumps(all_tasks_for_validation[0], ensure_ascii=False, indent=2))

# ===== 调用 LLM 一次性校验所有任务 =====
try:
    # 🔍 打印实际构造的 prompt
    formatted_messages = prompt.format_messages(
        task_and_result_batch=json.dumps(all_tasks_for_validation, ensure_ascii=False, indent=2)
    )
    print("\n📨 [DEBUG] 发送给 LLM 的消息列表:")
    for msg in formatted_messages:
        print(f"【{msg.type.upper()}】: {msg.content[:200]}...")

    response = llm.invoke(formatted_messages)
    print(f"\n🤖 [LLM RESPONSE] 原始返回内容:\n{response.content}")

    content = response.content.strip()

    # 去除代码块标记
    if content.startswith("```json"):
        content = content[7:-3].strip()
        print("🧹 [DEBUG] 已去除 ```json 包裹")
    elif content.startswith("```"):
        content = content[3:-3].strip()
        print("🧹 [DEBUG] 已去除 ``` 包裹")

    # 解析 JSON
    batch_result = json.loads(content)

    # ✅ 提取真正的校验结果列表
    verification_result_list = batch_result.get("verification_result", [])
    if not isinstance(verification_result_list, list):
        raise ValueError(f"LLM 返回的 'verification_result' 不是列表，而是 {type(verification_result_list)}")

    print(f"✅ [SUCCESS] JSON 解析成功，共 {len(verification_result_list)} 条结果")
    print("🔍 [DEBUG] LLM 返回的解析结果预览:", verification_result_list[:2])

except Exception as e:
    print(f"❌ [ERROR] LLM 批量校验失败: {str(e)}")
    # 回退：所有任务都失败
    verification_results = [
        {
            "agent_name": task["agent_name"],
            "section": task["section"],
            "subsection": task["subsection"],
            "request": task["request"],
            "status": "failed",
            "reason": f"[{task['agent_name']}] 批量校验调用失败: {str(e)}"
        }
        for task in all_tasks_for_validation
    ]
else:
    # 成功解析后的处理
    verification_results = []
    result_lookup = {
        (item.get("section"), item.get("subsection")): item
        for item in verification_result_list  # ✅ 正确遍历列表
        if isinstance(item, dict) and "section" in item and "subsection" in item
    }
    print(f"🔍 [DEBUG] LLM 返回中成功匹配的任务数: {len(result_lookup)}")

    for task in all_tasks_for_validation:
        key = (task["section"], task["subsection"])
        matched = result_lookup.get(key)

        if task.get("execution_result") is None:
            verification_results.append({
                "agent_name": task["agent_name"],
                "section": task["section"],
                "subsection": task["subsection"],
                "request": task["request"],
                "status": "failed",
                "reason": task["error"]
            })
        elif matched:
            verification_results.append({
                "agent_name": task["agent_name"],
                "section": matched.get("section", task["section"]),
                "subsection": matched.get("subsection", task["subsection"]),
                "request": task["request"],
                "status": matched.get("status", "failed"),
                "reason": matched.get("reason", "未提供原因")
            })
        else:
            verification_results.append({
                "agent_name": task["agent_name"],
                "section": task["section"],
                "subsection": task["subsection"],
                "request": task["request"],
                "status": "failed",
                "reason": f"[{task['agent_name']}] LLM 未返回该任务的校验结果"
            })

# ===== 统计结果 =====
verification_success_result = [r for r in verification_results if r["status"] == "success"]
verification_failed_result = [r for r in verification_results if r["status"] == "failed"]

if all(r["status"] == "success" for r in verification_results):
    verification_status = "ok"
    should_terminate = True
elif len(verification_success_result) > 0:
    verification_status = "again"
    should_terminate = False
else:
    verification_status = "again"
    should_terminate = False

return1 = {
    "verification_status": verification_status,
    "should_terminate": should_terminate,
    "verification_success_result": verification_success_result,
    "verification_failed_result": verification_failed_result,
    "messages": [AIMessage(content=f"✅ 检验器校验结束，总体检验结果：{verification_status}")],
}


print("\n🎯 [FINAL RETURN] 返回结果:")
print(f"verification_status: {return1['verification_status']}")
print(f"should_terminate: {return1['should_terminate']}")
print(f"成功任务数: {len(return1['verification_success_result'])}")
print(f"失败任务数: {len(return1['verification_failed_result'])}")
print(f"消息: {return1['messages'][0].content}")