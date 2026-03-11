from typing import TypedDict, Dict, Any, Optional, Annotated, List, Literal
from operator import add

StatusResult = Literal["success", "failed","skipped","partial_success"]
ValidationStatusType = Literal["ok", "again"]
def update_state(left, right):
    return right
def update_state2(left: dict, right: dict) -> dict:
    from copy import deepcopy

    result = deepcopy(left)

    for key, value in right.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = update_state(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result
def update_done_count(current: int, update: Optional[int]) -> int:
    if update is None:
        return current
    return current + update

class UserInputParsingResult(TypedDict, total=False):
    status: StatusResult
    data: Dict[str, Any]
    error: Optional[str]
class PaperParsingResult(TypedDict, total=False):
    status: StatusResult
    data: Any
    error: Optional[str]


class RequestGroupResult(TypedDict, total=False):
    section: str
    subsection: str
    request: Dict[str, Any]
    content: str

class AgentStatus(TypedDict, total=False):
    agent_mission: Any
    agent_result: Any

class VerificationItem(TypedDict, total=False):
    section: str
    subsection: str
    request: Dict[str, str]
    status: str
    reason: str

class MaingraphState(TypedDict, total=False):
    messages: Annotated[List[Dict[str, Any]], add]

    user_input: Annotated[Optional[List[str]], add]
    paper_file: Annotated[Optional[List[str]], "论文文件信息，未上传时为 None"]
    task_judgement: Annotated[Literal[True, False, "again"], "任务是否在服务范围内"]
    rejection_reason: Annotated[Optional[str], "拒绝或中断的原因"]

    user_input_parser: Annotated[Optional[UserInputParsingResult], "用户需求解析结果"]
    paper_file_parser: Annotated[Optional[PaperParsingResult], "论文内容解析结果"]
    request_group: Annotated[List[RequestGroupResult],update_state]

    input_parser_retry: Annotated[int, "重试次数"]
    paper_parser_retry: Annotated[int, "重试次数"]
    layout_check_retry: Annotated[int, "重试次数"]
    agent_carry_count: Optional[int]
    agent_done_count: Annotated[int,update_done_count]

    verification_status: Annotated[StatusResult, "整体验证状态"]
    verification_success_result: List[VerificationItem]
    verification_failed_result: List[VerificationItem]
    should_terminate: Annotated[bool, "是否终止流程"]

    final_status: Annotated[Optional[str], "最终状态"]
    final_paper: Annotated[Optional[str], "最终合成的论文"]
    awaiting : Optional[str]
    email:Annotated[Optional[str], "获取用户邮箱"]

    author: Annotated[AgentStatus, update_state2]
    chart: Annotated[AgentStatus, update_state2]
    cover: Annotated[AgentStatus, update_state2]
    fund: Annotated[AgentStatus, update_state2]
    reference: Annotated[AgentStatus, update_state2]
    text: Annotated[AgentStatus, update_state2]
    other: Annotated[AgentStatus, update_state2]

