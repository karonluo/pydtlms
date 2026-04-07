from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


from app.services.management_service import store
from app.schemas.recruitment import RecruitApplicationUpsert
from app.schemas.training import OutboundStudyUpsert, ScientificReportUpsert, ThesisUpsert


ADMIN_PRINCIPAL = {
    "username": "admin",
    "full_name": "系统管理员",
    "roles": ["platform_admin"],
    "permissions": ["*"],
}
ADVISOR_PRINCIPAL = {
    "username": "liu.ya",
    "full_name": "刘亚",
    "roles": ["advisor"],
    "permissions": ["*"],
}
SECRETARY_PRINCIPAL = {
    "username": "zhou.qing",
    "full_name": "周晴",
    "roles": ["secretary"],
    "permissions": ["*"],
}


def assert_equal(actual: Any, expected: Any, message: str) -> None:
    """校验实际值与预期值一致。

    功能说明:
        用于在模拟流程测试中校验关键状态、节点和业务字段是否符合预期。

    处理规则:
        当实际值与预期值不一致时，直接抛出 AssertionError，终止当前测试。

    Args:
        actual: 实际值。
        expected: 预期值。
        message: 断言失败时输出的说明。

    Returns:
        None。

    Raises:
        AssertionError: 当实际值与预期值不一致时抛出。
    """

    if actual != expected:
        raise AssertionError(f"{message}: expected={expected!r}, actual={actual!r}")


def assert_true(condition: bool, message: str) -> None:
    """校验布尔条件为真。

    功能说明:
        用于验证流程元数据、历史记录数量以及存在性检查等布尔型条件。

    处理规则:
        当条件为假时，直接抛出 AssertionError。

    Args:
        condition: 待校验条件。
        message: 断言失败时输出的说明。

    Returns:
        None。

    Raises:
        AssertionError: 当条件为假时抛出。
    """

    if not condition:
        raise AssertionError(message)


def get_task_by_business_key(business_key: str) -> dict[str, Any]:
    """根据业务编号定位流程任务。

    功能说明:
        从当前运行态 workflow_tasks 中查找与业务对象关联的流程任务记录。

    处理规则:
        若找不到对应任务，则抛出 AssertionError，说明流程未按预期创建。

    Args:
        business_key: 业务编号。

    Returns:
        dict[str, Any]: 匹配到的任务字典。

    Raises:
        AssertionError: 未找到对应业务编号任务时抛出。
    """

    located = store._workflow_task_index_by_business_key(business_key)
    if not located:
        raise AssertionError(f"未找到 business_key={business_key} 对应的流程任务")
    return located[1]


def expect_permission_error(task_id: int, action: str, principal: dict[str, Any], label: str) -> None:
    """校验错误角色无法执行当前流程动作。

    功能说明:
        用于验证不同角色只能执行其被授权的流程活动，满足审批角色隔离要求。

    处理规则:
        期望 store.execute_workflow_action 抛出 PermissionError；若未抛出则视为失败。

    Args:
        task_id: 任务 ID。
        action: 流程动作编码。
        principal: 执行人信息。
        label: 当前校验场景标签。

    Returns:
        None。

    Raises:
        AssertionError: 当未抛出 PermissionError 时抛出。
    """

    try:
        store.execute_workflow_action(task_id, action=action, comment=f"{label}-越权尝试", principal=principal)
    except PermissionError:
        return
    raise AssertionError(f"{label} 未按预期拦截越权操作")


def simulate_recruitment_flow() -> dict[str, Any]:
    """模拟招生录取审批正向流转。

    功能说明:
        创建报名申请，并依次执行资格审核、评分准备、面试安排、录取决策和录取确认。

    处理规则:
        所有节点均由 platform_admin 角色处理，同时校验最终业务状态与流程状态一致。

    Args:
        无。

    Returns:
        dict[str, Any]: 包含业务编号、最终状态和历史条数的结果摘要。

    Raises:
        AssertionError: 当任一流程断言失败时抛出。
    """

    created = store.create_recruitment_application(
        RecruitApplicationUpsert(
            plan_id=1,
            business_key=None,
            candidate_no=None,
            student_name="流程联调-招生申请",
            graduation_school="东南大学",
            highest_degree="硕士",
            intended_field="智能制造",
            material_status="材料齐全",
            application_status="报名已提交",
            reviewer_name=None,
            final_score=None,
        ),
        principal=ADMIN_PRINCIPAL,
    )
    assert_true(bool(created.business_key), "招生申请未生成 business_key")
    task = get_task_by_business_key(created.business_key)
    assert_equal(task.get("current_node"), "资格审核", "招生流程初始节点错误")
    assert_true(bool(task.get("process_instance_id")), "招生流程未生成流程实例元数据")

    result = store.execute_workflow_action(int(task["id"]), action="approve", comment="资格通过", principal=ADMIN_PRINCIPAL)
    assert_equal(result["task"].current_node, "评分准备", "招生流程资格审核后节点错误")

    result = store.execute_workflow_action(int(task["id"]), action="start_scoring", comment="启动评分", principal=ADMIN_PRINCIPAL)
    assert_equal(result["task"].current_node, "面试安排", "招生流程评分准备后节点错误")

    result = store.execute_workflow_action(int(task["id"]), action="schedule_interview", comment="完成安排", principal=ADMIN_PRINCIPAL)
    assert_equal(result["task"].current_node, "录取决策", "招生流程面试安排后节点错误")

    result = store.execute_workflow_action(int(task["id"]), action="record_interview", comment="录入结果", principal=ADMIN_PRINCIPAL)
    assert_equal(result["task"].current_node, "录取确认", "招生流程录取决策后节点错误")

    result = store.execute_workflow_action(int(task["id"]), action="admit", comment="同意录取", principal=ADMIN_PRINCIPAL)
    assert_equal(result["task"].status, "已通过", "招生流程最终任务状态错误")
    assert_equal(result["task"].current_node, "流程结束", "招生流程未结束")
    entity = next(item for item in store.state["recruitment_applications"] if item["business_key"] == created.business_key)
    assert_equal(entity["application_status"], "同意录取", "招生流程业务状态未同步")
    return {
        "flow": "recruitment_application",
        "scenario": "admit",
        "business_key": created.business_key,
        "final_status": entity["application_status"],
        "task_status": result["task"].status,
        "history_count": len(result["history"]),
    }


def simulate_scientific_report_flow() -> dict[str, Any]:
    """模拟科研报告审阅流程并验证角色隔离。

    功能说明:
        创建科研报告后先验证管理员不能越权审阅，再由导师执行审阅通过动作。

    处理规则:
        初始节点只能由 advisor 角色处理，最终状态应同步为已通过。

    Args:
        无。

    Returns:
        dict[str, Any]: 包含业务编号、最终状态和历史条数的结果摘要。

    Raises:
        AssertionError: 当角色校验或状态同步失败时抛出。
    """

    created = store.create_scientific_report(
        ScientificReportUpsert(
            business_key=None,
            student_no="D20240001",
            student_name="陈一鸣",
            period_label="2026Q2-模拟",
            report_status="待导师审阅",
            reviewer_name="刘亚",
            review_score=None,
            summary="流程联调科研报告摘要。",
        ),
        principal=ADVISOR_PRINCIPAL,
    )
    task = get_task_by_business_key(created.business_key)
    expect_permission_error(int(task["id"]), "approve", ADMIN_PRINCIPAL, "科研报告")
    result = store.execute_workflow_action(int(task["id"]), action="approve", comment="导师审阅通过", principal=ADVISOR_PRINCIPAL)
    entity = next(item for item in store.state["scientific_reports"] if item["business_key"] == created.business_key)
    assert_equal(entity["report_status"], "已通过", "科研报告业务状态未同步")
    assert_equal(result["task"].status, "已通过", "科研报告任务未通过")
    return {
        "flow": "scientific_report",
        "scenario": "approve",
        "business_key": created.business_key,
        "final_status": entity["report_status"],
        "task_status": result["task"].status,
        "history_count": len(result["history"]),
    }


def simulate_scientific_report_reject_flow() -> dict[str, Any]:
    """模拟科研报告退回修改场景。"""

    created = store.create_scientific_report(
        ScientificReportUpsert(
            business_key=None,
            student_no="D20240001",
            student_name="李知远",
            period_label="2026Q2-驳回模拟",
            report_status="待导师审阅",
            reviewer_name="刘亚",
            review_score=None,
            summary="用于验证科研报告退回修改分支。",
        ),
        principal=ADVISOR_PRINCIPAL,
    )
    task = get_task_by_business_key(created.business_key)
    result = store.execute_workflow_action(int(task["id"]), action="request_revision", comment="内容需补充", principal=ADVISOR_PRINCIPAL)
    entity = next(item for item in store.state["scientific_reports"] if item["business_key"] == created.business_key)
    assert_equal(entity["report_status"], "退回修改", "科研报告驳回分支业务状态未同步")
    assert_equal(result["task"].status, "已驳回", "科研报告驳回分支任务状态错误")
    return {
        "flow": "scientific_report",
        "scenario": "request_revision",
        "business_key": created.business_key,
        "final_status": entity["report_status"],
        "task_status": result["task"].status,
        "history_count": len(result["history"]),
    }


def simulate_outbound_study_flow() -> dict[str, Any]:
    """模拟外出研修审批串行双节点流转。

    功能说明:
        创建外出研修申请，依次由导师和平台管理员执行审批动作。

    处理规则:
        先验证秘书角色不能处理导师节点，再验证导师通过后流转到学合审核，最终由平台管理员审批通过。

    Args:
        无。

    Returns:
        dict[str, Any]: 包含业务编号、最终状态和历史条数的结果摘要。

    Raises:
        AssertionError: 当角色校验、节点流转或状态同步失败时抛出。
    """

    created = store.create_outbound_study(
        OutboundStudyUpsert(
            business_key=None,
            student_no="D20240007",
            student_name="王书宁",
            advisor_name="刘亚",
            study_type="联合培养",
            destination="新加坡国立大学",
            start_date="2026-07-01",
            end_date="2026-12-31",
            approval_status="审批中",
            expected_outcome="完成联合课题研究与论文投稿。",
        ),
        principal=ADVISOR_PRINCIPAL,
    )
    task = get_task_by_business_key(created.business_key)
    expect_permission_error(int(task["id"]), "approve", SECRETARY_PRINCIPAL, "外出研修导师节点")
    result = store.execute_workflow_action(int(task["id"]), action="approve", comment="导师同意", principal=ADVISOR_PRINCIPAL)
    assert_equal(result["task"].current_node, "学合审核", "外出研修未流转到学合审核")
    expect_permission_error(int(task["id"]), "approve", ADVISOR_PRINCIPAL, "外出研修学合节点")
    result = store.execute_workflow_action(int(task["id"]), action="approve", comment="平台审批通过", principal=ADMIN_PRINCIPAL)
    entity = next(item for item in store.state["outbound_studies"] if item["business_key"] == created.business_key)
    assert_equal(entity["approval_status"], "已批准", "外出研修业务状态未同步")
    assert_equal(result["task"].status, "已通过", "外出研修任务未通过")
    return {
        "flow": "outbound_study",
        "scenario": "approve",
        "business_key": created.business_key,
        "final_status": entity["approval_status"],
        "task_status": result["task"].status,
        "history_count": len(result["history"]),
    }


def simulate_outbound_study_reject_flow() -> dict[str, Any]:
    """模拟外出研修在学合审核节点被驳回。"""

    created = store.create_outbound_study(
        OutboundStudyUpsert(
            business_key=None,
            student_no="D20240007",
            student_name="林泽安",
            advisor_name="刘亚",
            study_type="短期访学",
            destination="东京大学",
            start_date="2026-08-01",
            end_date="2026-10-31",
            approval_status="审批中",
            expected_outcome="验证外出研修驳回分支。",
        ),
        principal=ADVISOR_PRINCIPAL,
    )
    task = get_task_by_business_key(created.business_key)
    result = store.execute_workflow_action(int(task["id"]), action="approve", comment="导师同意", principal=ADVISOR_PRINCIPAL)
    assert_equal(result["task"].current_node, "学合审核", "外出研修驳回场景未流转到学合审核")
    result = store.execute_workflow_action(int(task["id"]), action="reject", comment="材料不完整", principal=ADMIN_PRINCIPAL)
    entity = next(item for item in store.state["outbound_studies"] if item["business_key"] == created.business_key)
    assert_equal(entity["approval_status"], "已驳回", "外出研修驳回分支业务状态未同步")
    assert_equal(result["task"].status, "已驳回", "外出研修驳回分支任务状态错误")
    return {
        "flow": "outbound_study",
        "scenario": "reject",
        "business_key": created.business_key,
        "final_status": entity["approval_status"],
        "task_status": result["task"].status,
        "history_count": len(result["history"]),
    }


def simulate_thesis_flow() -> dict[str, Any]:
    """模拟学位申请审批双角色流转。

    功能说明:
        创建论文主档后，先由导师执行送审动作，再由学位秘书执行复核通过。

    处理规则:
        初始节点只能由 advisor 角色执行，秘书节点只能由 secretary 角色执行，最终业务状态应变为待正式答辩。

    Args:
        无。

    Returns:
        dict[str, Any]: 包含业务编号、最终状态和历史条数的结果摘要。

    Raises:
        AssertionError: 当角色隔离、节点流转或状态同步失败时抛出。
    """

    created = store.create_thesis(
        ThesisUpsert(
            business_key=None,
            student_no="D20230018",
            student_name="张乐之",
            advisor_name="袁野",
            title="流程联调论文主档",
            plagiarism_rate=8.6,
            thesis_status="待查重",
            blind_review_status="未送审",
            defense_status="待安排",
            degree_status="待申请",
        ),
        principal=ADVISOR_PRINCIPAL,
    )
    task = get_task_by_business_key(created.business_key)
    expect_permission_error(int(task["id"]), "submit_review", ADMIN_PRINCIPAL, "学位申请导师预审")
    result = store.execute_workflow_action(int(task["id"]), action="submit_review", comment="提交送审", principal=ADVISOR_PRINCIPAL)
    assert_equal(result["task"].current_node, "材料复核", "学位申请未流转到秘书复核")
    expect_permission_error(int(task["id"]), "approve", ADVISOR_PRINCIPAL, "学位申请秘书复核")
    result = store.execute_workflow_action(int(task["id"]), action="approve", comment="秘书复核通过", principal=SECRETARY_PRINCIPAL)
    entity = next(item for item in store.state["theses"] if item["business_key"] == created.business_key)
    assert_equal(entity["degree_status"], "待正式答辩", "学位申请业务状态未同步")
    assert_equal(entity["blind_review_status"], "已通过", "学位申请盲审状态未同步")
    assert_equal(result["task"].status, "已通过", "学位申请任务未通过")
    return {
        "flow": "thesis",
        "scenario": "approve",
        "business_key": created.business_key,
        "final_status": entity["degree_status"],
        "task_status": result["task"].status,
        "history_count": len(result["history"]),
    }


def simulate_thesis_reject_flow() -> dict[str, Any]:
    """模拟学位申请在秘书复核节点被驳回。"""

    created = store.create_thesis(
        ThesisUpsert(
            business_key=None,
            student_no="D20230018",
            student_name="顾行川",
            advisor_name="袁野",
            title="流程联调论文主档-驳回",
            plagiarism_rate=11.2,
            thesis_status="待查重",
            blind_review_status="未送审",
            defense_status="待安排",
            degree_status="待申请",
        ),
        principal=ADVISOR_PRINCIPAL,
    )
    task = get_task_by_business_key(created.business_key)
    result = store.execute_workflow_action(int(task["id"]), action="submit_review", comment="提交送审", principal=ADVISOR_PRINCIPAL)
    assert_equal(result["task"].current_node, "材料复核", "学位申请驳回场景未流转到秘书复核")
    result = store.execute_workflow_action(int(task["id"]), action="reject", comment="材料需补充", principal=SECRETARY_PRINCIPAL)
    entity = next(item for item in store.state["theses"] if item["business_key"] == created.business_key)
    assert_equal(entity["degree_status"], "未授位", "学位申请驳回分支业务状态未同步")
    assert_equal(entity["blind_review_status"], "未通过", "学位申请驳回分支盲审状态未同步")
    assert_equal(result["task"].status, "已驳回", "学位申请驳回分支任务状态错误")
    return {
        "flow": "thesis",
        "scenario": "reject",
        "business_key": created.business_key,
        "final_status": entity["degree_status"],
        "task_status": result["task"].status,
        "history_count": len(result["history"]),
    }


def simulate_recruitment_reject_flow() -> dict[str, Any]:
    """模拟招生流程在资格审核节点被驳回。"""

    created = store.create_recruitment_application(
        RecruitApplicationUpsert(
            plan_id=1,
            business_key=None,
            candidate_no=None,
            student_name="流程联调-招生驳回",
            graduation_school="哈尔滨工业大学",
            highest_degree="硕士",
            intended_field="工业软件",
            material_status="材料待补充",
            application_status="报名已提交",
            reviewer_name=None,
            final_score=None,
        ),
        principal=ADMIN_PRINCIPAL,
    )
    task = get_task_by_business_key(created.business_key)
    result = store.execute_workflow_action(int(task["id"]), action="reject", comment="资格不符", principal=ADMIN_PRINCIPAL)
    entity = next(item for item in store.state["recruitment_applications"] if item["business_key"] == created.business_key)
    assert_equal(entity["application_status"], "不录取", "招生驳回分支业务状态未同步")
    assert_equal(result["task"].status, "已驳回", "招生驳回分支任务状态错误")
    return {
        "flow": "recruitment_application",
        "scenario": "reject",
        "business_key": created.business_key,
        "final_status": entity["application_status"],
        "task_status": result["task"].status,
        "history_count": len(result["history"]),
    }


def main() -> None:
    """执行审批流程模拟验证并在结束后恢复运行态。

    功能说明:
        依次模拟四类托管流程，输出每条流程的执行摘要，并在 finally 中恢复原始状态。

    处理规则:
        使用深拷贝保存运行态快照；无论执行成功还是失败，都会恢复 PostgreSQL runtime state。

    Args:
        无。

    Returns:
        None。

    Raises:
        Exception: 任一流程执行异常时原样抛出，供外部命令行识别失败。
    """

    original_state = copy.deepcopy(store.state)
    results: list[dict[str, Any]] = []
    try:
        results.append(simulate_recruitment_flow())
        results.append(simulate_recruitment_reject_flow())
        results.append(simulate_scientific_report_flow())
        results.append(simulate_scientific_report_reject_flow())
        results.append(simulate_outbound_study_flow())
        results.append(simulate_outbound_study_reject_flow())
        results.append(simulate_thesis_flow())
        results.append(simulate_thesis_reject_flow())
        print(json.dumps({"success": True, "results": results}, ensure_ascii=False, indent=2))
    finally:
        store.state = copy.deepcopy(original_state)
        store._counters = store.state.setdefault("counters", {})
        store._write_state(store.state)


if __name__ == "__main__":
    main()