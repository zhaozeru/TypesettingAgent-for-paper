from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from state.schema import MaingraphState
from agent import (author_node,chart_node,cover_node,fund_node,input_parser_node,paper_parser_node,reference_node,text_node,validator_node,layout_agent_node,input_check_node,parser_check_node,layout_check_node,other_node,assemble_node,human_editing_node,send_email_node)
from langgraph.constants import END, START
from graph.routes import routing_func1, routing_func2,routing_func3,routing_func4,subrouting_func1


def create_formatting_graph():
    subgraph_builder = StateGraph(MaingraphState)

    subgraph_builder.add_node("author", author_node)
    subgraph_builder.add_node("chart", chart_node)
    subgraph_builder.add_node("cover", cover_node)
    subgraph_builder.add_node("fund", fund_node)
    subgraph_builder.add_node("reference", reference_node)
    subgraph_builder.add_node("text", text_node)
    subgraph_builder.add_node("other", other_node)

    subgraph_builder.add_conditional_edges(
        START,
        subrouting_func1,
        ["author", "chart", "cover", "fund", "reference", "text", "other"],
    )
    subgraph_builder.add_edge("author", END)
    subgraph_builder.add_edge("chart", END)
    subgraph_builder.add_edge("cover", END)
    subgraph_builder.add_edge("fund", END)
    subgraph_builder.add_edge("reference", END)
    subgraph_builder.add_edge("text", END)
    subgraph_builder.add_edge("other", END)

    subgraph = subgraph_builder.compile()

    # 主图
    builder = StateGraph(MaingraphState)
    # 点
    builder.add_node("input_check", input_check_node)
    builder.add_node("parser_check", parser_check_node)
    builder.add_node("layout_check", layout_check_node)
    builder.add_node("paper_parser", paper_parser_node)
    builder.add_node("input_parser", input_parser_node)
    builder.add_node("layout_agent", layout_agent_node)
    builder.add_node("tool_agent", subgraph)
    builder.add_node("validator", validator_node)
    builder.add_node("assemble", assemble_node)
    builder.add_node("human_editing", human_editing_node)
    builder.add_node("send_email", send_email_node)


    # 边
    builder.add_edge(START, "input_check")
    builder.add_conditional_edges(
        "input_check",
        routing_func1,
        ["input_check","input_parser","paper_parser",END]
    )
    builder.add_conditional_edges("input_parser", routing_func2,["parser_check","input_parser"])
    builder.add_conditional_edges("paper_parser", routing_func3,["parser_check","paper_parser"])
    builder.add_edge("parser_check", "layout_check")
    builder.add_conditional_edges(
        "layout_check",
        routing_func4,
        ["layout_agent","validator","assemble",END])
    builder.add_edge("layout_agent", "tool_agent")
    builder.add_edge("tool_agent", "layout_check")
    builder.add_edge("validator", "layout_check")
    builder.add_edge("assemble", "human_editing")
    builder.add_edge("human_editing", "send_email")
    builder.add_edge("send_email", END)

    checkpointer = InMemorySaver() # 开发环境可以保存在内容，生产环境要找个数据库来存
    graph = builder.compile(checkpointer=checkpointer)

    return graph
