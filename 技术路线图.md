# 论文排版智能体助手 - 项目实现路线图


## 🎯 项目目标
- **输入**：
  - 有排版需求的论文原文（`.docx` 文件或文本）
  - 排版要求是指不同期刊要求的论文格式模版（以自然语言文字描述，例如：“标题用黑体三号，正文宋体小四，1.5倍行距”）
- **输出**：
  - 格式正确的 `.docx` 文件，符合期刊要求的学术排版规范


## 📝 说明
- 本项目采用 **LangGraph** 作为核心框架，构建一个具备状态管理、可干预的多智能体协同框架。
- 配合LLM调用与Tools绑定，来实现具体工具任务。
- 整个流程涉及到了多个功能，比如人类干预、Graph循环、条件边判断、主图与子图、上下文记忆等。

## 🌊 LangGraph流程图
![LangGraph流程图](./论文排版agent流程图.drawio.svg)
## 🗺️ 实现路线图（分阶段）

---
### ✅ 阶段 0：环境准备与项目初始化

| 任务 | 说明 | 产出 |
|------|------|------|
| 🔧 安装依赖 | `pip install langchain langgraph python-docx openai zhipuai dashscope redis` | `requirements.txt` |
| 📁 创建项目目录 | 按照优化后的模块化结构初始化目录 | 完整的文件夹结构 |
| 🎯 初始化 `main.py` | 创建空入口，准备调用 `graph.stream()` | 可运行的启动脚本 |
| ⚙️ 配置 API Key | 在 `.env` 或 `config/settings.py` 中设置 `ZHIPUAI_API_KEY` | 安全的配置管理 |

### 🚧 阶段 1：基础工具开发（Tools Layer）
| 任务 | 说明 | 产出 |
|-----|------|------|
|实现 `tools/docx_tool.py` | 提供 `read_docx`, `format_text_in_docx`, `add_paragraph`, `set_font` 等函数 | 可复用的 Word 操作工具 |
|实现 `tools/utils.py` | 路径处理、文件存在性检查、文本提取等辅助函数 | 工具函数库 |
|单元测试 | 编写测试用例验证 `docx_tool.py` 功能 | `test_docx_tool.py`（可选） |

### 🚧 阶段 2：智能体节点开发（Agents Layer）
| 模块 | 任务 | 说明 |
|------|------|------|
| **`agents/parser.py`** | 实现 `parser_node` | 将用户指令（如“把摘要加粗”）解析为结构化规则 `{field: "abstract", format: {bold: True}}` |
| **`agents/formatter.py`** | 实现 `formatter_node` | 调用 `docx_tool` 执行排版，支持 `create_react_agent` 调用工具 |
| **`agents/validator.py`** | 实现 `validator_node` | 检查排版结果是否符合要求，返回 `is_valid: bool` 和 `feedback: str` |
| **`agents/supervisor.py`** | 实现 `supervisor_node` | 任务分类器：根据用户输入决定走 `parse → format → validate` 还是 `other` 分支 |

> ✅ 所有节点输出 `{"messages": [...], "type": "next_node"}` 结构，供路由使用。

### 🚧 阶段 3：状态与图结构定义（State & Graph）
| 模块 | 任务 | 说明 |
|------|------|------|
| **`state/schema.py`** | 定义 `State(TypedDict)` | 包含 `messages`, `parsed_rules`, `type`, `retry_count` 等字段 |
| **`graph/builder.py`** | 构建 `StateGraph` | 添加节点、边，设置初始节点为 `supervisor_node` |
| **`graph/routes.py`** | 实现 `routing_func` | 根据 `state.type` 路由到 `parser_node`, `formatter_node`, `validator_node` 或 `END` |
| **`memory/checkpoint.py`** | 配置 `InMemorySaver()` | 支持对话记忆，便于调试和恢复 |

### 🚧 阶段 4：提示词工程与 Tool绑定（Prompts & Tool）
| 任务 | 说明 | 产出 |
|------|------|------|
| 📝 编写 `prompts/*.txt` | 为每个节点编写外部化 prompt（如 `parser_prompt.txt`） | 可调试、可 A/B 测试的提示词 |
| 🔍 实现 RAG 增强 | 使用 `dashscope` 向量模型将用户指令与“排版规则库”匹配 | 提升指令解析准确率 |
| 🗃️ 构建 `vectorstore/` | 存储常见指令-规则对（如“加粗”→`{"bold": true}`） | 支持语义检索 |

> ✅ 示例：`parser_prompt.txt`
```
你是一个论文排版指令解析器，请将用户指令转化为结构化 JSON。
支持字段：title, abstract, keywords, section, paragraph, format: {bold, italic, font, size}
示例输入：“把摘要加粗” → {"field": "abstract", "format": {"bold": true}}
```

### 🚧 阶段 5：主流程集成与流式输出
| 任务 | 说明 | 产出 |
|------|------|------|
| 🖱️ 完善 `main.py` | 初始化 `llm`, `saver`, `graph`，调用 `stream()` | 可运行的主程序 |
| 📡 实现流式输出 | 使用 `get_stream_writer()` 实时打印每个节点执行 | 可视化调试体验 |
| 📤 输入输出测试 | 传入 `raw_paper.docx`，执行指令，生成 `formatted_paper.docx` | 端到端验证 |

### 🚀 阶段 6：优化与扩展（高级功能）
| 任务 | 说明 |
|------|------|
| 🔁 失败重试机制 | `validator_node` 发现错误时，`retry_count < 3` 则返回 `parser_node` |
| 🧠 持久化记忆 | 将 `InMemorySaver` 替换为 `RedisSaver`，支持长期对话 |
| 📎 支持 PDF/图片 | 集成 OCR 工具（如 `PaddleOCR`）处理扫描版论文 |
| 👥 人工审核节点 | 增加 `review_node`，关键修改前确认 |
| 📊 日志与监控 | 使用 `utils/logger.py` 记录执行过程，便于追踪 |

### 🏁 阶段 7：打包与部署（可选）
| 任务 | 说明 |
|------|------|
| 📦 封装为 CLI 工具 | 支持命令行调用：`python main.py --input paper.docx --instruction "加粗标题"` |
| 🌐 Web 界面（Gradio/Streamlit） | 用户上传文件 + 输入指令，实时查看排版过程 |
| ☁️ 部署为 API 服务 | 使用 FastAPI 封装，供其他系统调用 |

## 📊 路线图总览（甘特图式）
| 阶段 | 时间建议 | 依赖关系 |
|------|--------|----------|
| 0️⃣ 环境准备 | Day 1 | 无 |
| 1️⃣ 工具开发 | Day 2 | 0️⃣ |
| 2️⃣ 智能体节点 | Day 3-4 | 1️⃣ |
| 3️⃣ 状态与图 | Day 5 | 2️⃣ |
| 4️⃣ 提示词与 RAG | Day 6 | 3️⃣ |
| 5️⃣ 主流程集成 | Day 7 | 4️⃣ |
| 6️⃣ 优化扩展 | Day 8-10 | 5️⃣ |
| 7️⃣ 打包部署 | Day 11+ | 6️⃣ |


