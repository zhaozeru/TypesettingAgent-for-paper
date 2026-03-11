# 与大语言模型交互
from langchain.chains import llm
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(
    model=llm,
    tools=[],
    prompt="You are a helpful assisant",)
agent.invoke({"messages": [{"role": "user", "content": "你是谁？"}]})


# 支持常用的流式输出
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "你是谁？"}]}, stream_mode="messages"):
    print(chunk)
    print("\n")


# Tool工具示例
import datetime
def get_current_date():
    """获取今天日期"""
    return datetime.datetime.today().strftime("%Y-%m-%d")


# 记忆模块下的短期记忆示例
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
checkpoint = InMemorySaver()
def get_weather(city: str) -> str:
    """获取某个城市的天气"""
    return f"城市：{city}, 天气一直都是晴天！"
agent = create_react_agent(
    model=llm,
    tools=[get_weather],
    checkpoint=checkpoint,)
config = {"configurable": {"thread_id": "1"}}
cs_response = agent.invoke(
    {"messages": [{"role": "user", "content": "长沙的天气怎么样？"}]}, config)


# LangGraph中Graph图的建立
from typing import TypedDict
from langgraph.constants import END,START
from langgraph.graph import StateGraph
class InputState(TypedDict):
    user_input: str
class OutputState(TypedDict):
    graph_output: str
class OverallState(TypedDict):
    foo:str
    User_input: str
    graph_output: str
class PrivateState(TypedDict):
    bar:str

def node_1(state:InputState) -> OverallState:
    return {"foo": state["user_input"] + ">学院"}
def node_2(state:OverallState) -> PrivateState:
    return {"bar": state["foo"] + ">非常"}
def node_3(state:PrivateState) -> OutputState:
    return {"graph_output": state["bar"] + ">靠谱"}

builder = StateGraph(OverallState, input=InputState, output=OutputState)
builder.add_node('node_1', node_1)
builder.add_node('node_2', node_2)
builder.add_node('node_3', node_3)
builder.add_edge(START, 'node_1')
builder.add_edge('node_1', 'node_2')
builder.add_edge('node_2', 'node_3')
builder.add_edge('node_3', END)
graph = builder.compile()
graph.invoke({"user_input": "图灵"})


# 以图的形式将上面代码展示
png_data = graph.get_graph().draw_mermaid_png() # 把图像保存下来查看
with open("graph.png", "wb") as f:
    f.write(png_data)
print("✅ 图像已保存：请查看项目目录下的 graph.png")


# State更新示例
from langchain_core.messages import AngMessage, AIMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated
from operator import add
class State(TypedDict):
    message: Annotated[list[AngMessage], add_messages]
    list_field: Annotated[list[int], add]
    extra_field: int
def node1(state:State):
    new_message = AIMessage('hello!')
    return {"message": [new_message], "list_field": [10], "extra_field": 2}
def node2(state:State):
    new_message = AIMessage('LangGraph!')
    return {"message": [new_message], "list_field": [20], "extra_field": 20}
graph = (StateGraph(State)
         .add_node('node1', node1)
         .add_node('node2', node2)
         .set_entry_point('node1')
         .add_edge('node1', 'node2')
         .compile())
input_message = {"role":"user", 'content':"Hi"}
result = graph.invoke({"messages":[input_message], "list_field":[1,2,3]})


# Node创建示例
from typing import TypedDict
import time
from langchain_core.runnables import RunnableConfig
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import CachePolicy
from langgraph.cache.memory import InMemoryCache
class State(TypedDict):
    number : int
    user_id : str
class ConfigSchema(TypedDict):
    user_id : str
def node_1(state:State, config:RunnableConfig):
    time.sleep(3)
    user_id = config['configurable']['user_id']
    return {"number": state['number'] + 1, "user_id": user_id}
builder = StateGraph(State, config_schema=ConfigSchema)
builder.add_node('node1', node_1,ceche_policy=CachePolicy(ttl=5))
builder.add_edge(START, 'node1')
builder.add_edge('node1', END)
graph = builder.compile(cache=InMemoryCache())
print(graph.invoke({"number":5}, config={"configurable":{"user_id":"123"}},stream_mode='updates'))
print(graph.invoke({"number":5}, config={"configurable":{"user_id":"456"}},stream_mode='updates'))


# Node补充用法
from langgraph.types import RetryPolicy
builder.add_node("node1", node_1, retry=RetryPolicy(max_attempts=4)) # 重试机制
print(graph.invoke('xxxxx', config={"recursion_limit":25})) # 针对某一次任务调用指令


# Edge创建
class State(TypedDict):
    number : int
def node_1(state:State, config:RunnableConfig):
    return {"number": state["number"] + 1}
builder.add_node("node1", node_1)
def routing_func(state:State) -> str:
    if state["number"] > 5:
        return True
    else:
        return False
builder.add_edge("node1", END)
builder.add_conditional_edges(START, routing_func, {True:'node_1', False:'node_2'})
graph = builder.compile()
print(graph.invoke({'number':4}))


# Edge,send命令
class State(TypedDict):
    messages: Annotated[list[str], add]
class PrivateState(TypedDict):
    msg:str
def node_1(state:PrivateState) -> State:
    res = state['msg']+'!'
    return {"messages":[res]}
builder = StateGraph(State)
builder.add_node("node1",node_1)
def routing_func(state:State):
    result=[]
    for message in state['messages']:
        result.append(Send("node1", {'msg':message}))
    return result
builder.add_conditional_edges(START, routing_func, {'node1'})
builder.add_edge('node1', END)
graph=builder.compile()
print(graph.invoke({'messages':['heool','graph']}))


# Edge, command命令,是send的升级版
class State(TypedDict):
    messages: Annotated[list[str], add]
def node_1(state:State):
    new_message = []
    for message in state['messages']:
        new_message.append(message+'!')
    return Command(
        goto=END,
        update={'messages':new_message}
    )
builder = StateGraph(State)
builder.add_node('node1',node_1)
builder.add_edge(START, 'node1')
graph=builder.compile()
print(graph.invoke({'message':['hello','world']}))


# Edge,子图示例
class State(TypedDict):
    messages: Annotated[list[str], add]
def sub_node_1(state:State) -> MessagesState:
    return {'messages':['response from subgraph']}
subgraph_builder = StateGraph(State)
subgraph_builder.add_node('sub_node_1',sub_node_1)
subgraph_builder.add_edge(START, "sub_node_1")
subgraph_builder.add_edge('sub_node_1', END)
subgraph = subgraph_builder.compile()
builder = StateGraph(State)
builder.add_node('subgraph_node',subgraph)
builder.add_edge(START, 'subgraph_node')
builder.add_edge('subgraph_node', END)
graph = builder.compile()
print(graph.invoke({'messages':['hello subgraph']}))