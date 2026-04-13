from __future__ import annotations

from datetime import datetime
import json
import sys
from pathlib import Path
from typing import Any


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.core.config import settings
from app.schemas.training import ThesisUpsert
from app.services.management_service import store
from app.services.postgres_state_store import PostgresStateStore


def _principal(username: str) -> dict[str, Any]:
    """读取真实用户对应的权限上下文。

    功能说明:
        基于当前运行态系统用户主数据，获取指定用户名的真实角色与权限，
        作为流程动作执行人，避免使用硬编码的伪造身份。

    处理规则:
        若用户名不存在，则直接抛出异常，阻止生成与主数据不一致的模拟记录。

    Args:
        username: 系统用户登录名。

    Returns:
        dict[str, Any]: 包含 username、full_name、roles、permissions 的执行上下文。

    Raises:
        KeyError: 当用户不存在时抛出。
    """

    return store.get_principal_context(username)


def _student(student_no: str) -> dict[str, Any]:
    """按学号读取现有学生主数据。"""

    for item in store._list("students"):
        if item.get("student_no") == student_no:
            return item
    raise KeyError(f"未找到 student_no={student_no} 对应的学生主数据")


def _task_by_business_key(business_key: str) -> dict[str, Any]:
    """根据业务编号定位流程任务。"""

    located = store._workflow_task_index_by_business_key(business_key)
    if not located:
        raise KeyError(f"未找到 business_key={business_key} 对应的流程任务")
    return located[1]


def _db_history_count(business_key: str) -> int:
    """统计 Flowable 兼容历史表中某业务编号的活动数。"""

    postgres_store = PostgresStateStore()
    with postgres_store._connect(settings.postgres_db) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM dtlms_wf_hi_actinst WHERE business_key_ = %s",
                (business_key,),
            )
            row = cur.fetchone()
            return int(row[0]) if row else 0


def main() -> None:
    """生成一条走完学位业务与审批流程的模拟数据。

    功能说明:
        复用现有学生、导师、学位秘书等真实主数据，创建一条新的论文主档，
        然后依次完成导师预审与学位秘书复核，形成完整闭环的已通过流程数据。

    处理规则:
        1. 使用现有学生主数据沈知遥与其真实导师徐素天。
        2. 流程第二节点使用真实学位秘书周晴处理。
        3. 所有状态推进均通过 workflow 动作完成，确保业务状态、任务状态和历史记录同步落库。

    Args:
        无。

    Returns:
        None。

    Raises:
        Exception: 生成过程中的任何异常将原样抛出，便于命令行定位失败原因。
    """

    advisor_principal = _principal("xu.sutian")
    secretary_principal = _principal("zhou.qing")
    student = _student("D20230006")
    suffix = datetime.now().strftime("%Y%m%d%H%M%S")

    created = store.create_thesis(
        ThesisUpsert(
            business_key=None,
            student_no=student["student_no"],
            student_name=student["full_name"],
            advisor_name=student["advisor_name"],
            title=f"{student['full_name']}学位申请闭环模拟-{suffix}",
            plagiarism_rate=7.8,
            thesis_status="待查重",
            blind_review_status="未送审",
            defense_status="待安排",
            degree_status="待申请",
        ),
        principal=advisor_principal,
    )

    task = _task_by_business_key(created.business_key)
    first_result = store.execute_workflow_action(
        int(task["id"]),
        action="submit_review",
        comment="导师完成预审并提交送审",
        principal=advisor_principal,
    )
    second_result = store.execute_workflow_action(
        int(task["id"]),
        action="approve",
        comment="学位秘书复核通过",
        principal=secretary_principal,
    )
    detail = store.get_workflow_task_detail(int(task["id"]), principal=secretary_principal)
    thesis = next(item for item in store._list("theses") if item.get("business_key") == created.business_key)

    summary = {
        "business_key": created.business_key,
        "thesis_id": created.id,
        "student_no": thesis["student_no"],
        "student_name": thesis["student_name"],
        "advisor_name": thesis["advisor_name"],
        "title": thesis["title"],
        "degree_status": thesis["degree_status"],
        "thesis_status": thesis["thesis_status"],
        "blind_review_status": thesis["blind_review_status"],
        "workflow_name": detail["task"].workflow_name,
        "task_status": detail["task"].status,
        "current_node": detail["task"].current_node,
        "created_node_after_first_action": first_result["task"].current_node,
        "history_count": len(detail["history"]),
        "history": detail["history"],
        "db_history_activity_count": _db_history_count(created.business_key),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()