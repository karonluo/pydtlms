from __future__ import annotations

import logging
import smtplib
import ssl
from collections.abc import Callable
from threading import Thread
from email.message import EmailMessage

from app.core.config import Settings, settings


logger = logging.getLogger(__name__)


class NotificationEmailService:
    def __init__(self, settings_obj: Settings | None = None, log_delivery: Callable[..., None] | None = None) -> None:
        self._settings = settings_obj or settings
        self._log_delivery = log_delivery

    def enabled(self) -> bool:
        return bool(
            self._settings.smtp_enabled
            and self._settings.smtp_host
            and self._settings.smtp_port
            and self._settings.smtp_from_email
        )

    def workflow_notifications_enabled(self) -> bool:
        return bool(self.enabled() and self._settings.smtp_student_notification_enabled)

    def send_portal_registration_success(self, full_name: str, email: str) -> None:
        subject = "申请系统注册成功通知"
        text_body = (
            f"{full_name}，您好：\n\n"
            "您已成功注册上海人工智能实验室联培博士生申请系统账号。"
            "后续可使用注册手机号或邮箱登录系统并继续完善报名信息。\n\n"
            f"登录账号：{email}\n\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(to_email=email, subject=subject, text_body=text_body, template_code="portal_registration_success")

    def send_portal_registration_success_async(self, full_name: str, email: str) -> None:
        self._dispatch_async(self.send_portal_registration_success, full_name, email)

    def send_portal_registration_verification_code(self, email: str, verification_code: str) -> None:
        subject = "申请系统邮箱验证码"
        text_body = (
            "您好：\n\n"
            "您正在进行上海人工智能实验室联培博士生申请系统注册。\n"
            f"本次邮箱验证码为：{verification_code}\n"
            "验证码 10 分钟内有效，请勿泄露给他人。\n\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(to_email=email, subject=subject, text_body=text_body, template_code="portal_registration_verification_code")

    def send_portal_login_verification_code(self, email: str, verification_code: str) -> None:
        subject = "申请系统登录验证码"
        text_body = (
            "您好：\n\n"
            "您正在使用邮箱验证码登录上海人工智能实验室联培博士生申请系统。\n"
            f"本次邮箱验证码为：{verification_code}\n"
            "验证码 10 分钟内有效，请勿泄露给他人。\n\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(to_email=email, subject=subject, text_body=text_body, template_code="portal_login_verification_code")

    def send_portal_password_reset_success(self, full_name: str, email: str, account: str) -> None:
        subject = "申请系统密码重置成功通知"
        text_body = (
            f"{full_name}，您好：\n\n"
            "您的上海人工智能实验室联培博士生申请系统密码已成功重置。"
            "请尽快使用新密码重新登录，并妥善保管账号信息。\n\n"
            f"重置账号：{account}\n\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(to_email=email, subject=subject, text_body=text_body, template_code="portal_password_reset_success")

    def send_portal_admin_password_reset(self, full_name: str, email: str, temporary_password: str) -> None:
        subject = "申请系统密码重置通知"
        text_body = (
            f"{full_name}，您好：\n\n"
            "管理员已为您重置上海人工智能实验室联培博士生申请系统登录密码，请尽快登录后修改为您自己的密码。\n\n"
            f"临时密码：{temporary_password}\n\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(to_email=email, subject=subject, text_body=text_body, template_code="portal_admin_password_reset")

    def send_recruitment_status_update(
        self,
        *,
        student_name: str,
        email: str,
        business_key: str,
        application_status: str,
        plan_name: str | None = None,
        review_comment: str | None = None,
    ) -> None:
        subject = f"招生申请状态更新通知：{application_status}"
        plan_line = f"招生计划：{plan_name}\n" if plan_name else ""
        normalized_comment = str(review_comment or "").strip()
        comment_line = ""
        if application_status in {"驳回重填", "不录取", "报名终止"} and normalized_comment:
            comment_line = f"原因：{normalized_comment}\n"
        guidance_map = {
            "资格审核通过": "您的申请已通过资格审核，后续请留意系统中的后续安排。\n",
            "待导师初筛": "您的申请已通过背景评估，正在等待进入导师初筛环节，请留意系统、邮件或电话通知。\n",
            "待导师初筛-第一志愿": "您的申请已通过背景评估，当前正在等待第一志愿导师完成初筛评分，系统将按 80 分阈值自动判定结果，请留意系统、邮件或电话通知。\n",
            "待导师初筛-第二志愿": "您的申请已进入第二志愿导师初筛阶段，导师完成评分后系统将按 80 分阈值自动判定结果，请留意系统、邮件或电话通知。\n",
            "待初筛确认": "您的导师初筛已完成，当前正在等待书院管理员完成初筛确认，请留意系统通知。\n",
            "入营面试": "您的申请已通过初筛，已进入入营面试环节，请留意系统、邮件或电话通知。\n",
            "预录取": "您的申请已进入预录取阶段，请关注后续确认通知。\n",
            "同意录取": "您的申请已确认录取，请按后续通知完成相关手续。\n",
            "驳回重填": "您的申请已被驳回重填，请登录系统补充或修改信息后重新提交。\n",
            "不录取": "很遗憾，本次申请未获通过。如需继续申请，请重新登录系统补充并重新提交申报内容。\n",
            "报名终止": "很遗憾，您的申请在当前环节未通过评估，本次报名流程已终止。\n",
        }
        guidance_line = guidance_map.get(application_status, "请及时登录系统查看最新进展。\n")
        text_body = (
            f"{student_name}，您好：\n\n"
            "您的招生申请状态已更新，请及时登录系统查看。\n\n"
            f"业务编号：{business_key}\n"
            f"当前状态：{application_status}\n"
            f"{comment_line}"
            f"{guidance_line}"
            f"{plan_line}\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(
            to_email=email,
            subject=subject,
            text_body=text_body,
            template_code="recruitment_status_update",
            business_key=business_key,
        )

    def send_recruitment_material_review_rejection(
        self,
        *,
        student_name: str,
        email: str,
        business_key: str,
        application_status: str | None = None,
        plan_name: str | None = None,
        review_comment: str | None = None,
    ) -> None:
        subject = "招生申请状态更新通知：驳回"
        normalized_comment = str(review_comment or "").strip()
        plan_line = f"招生计划: {str(plan_name or '').strip()}\n" if str(plan_name or "").strip() else ""
        text_body = (
            f"{student_name}同学，您好:\n"
            "您的招生申请状态已更新，请及时登录系统查看。\n"
            f"业务编号: {business_key}\n"
            "当前状态：驳回\n"
            f"原因：{normalized_comment or '无'}\n"
            "您的申请已被驳回，请于 24H 内登录系统补充或修改信息后重新提交。\n"
            f"{plan_line}"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(
            to_email=email,
            subject=subject,
            text_body=text_body,
            template_code="recruitment_material_review_rejection",
            business_key=business_key,
        )

    def send_recruitment_stage_rollback(
        self,
        *,
        student_name: str,
        email: str,
        business_key: str,
        target_stage_label: str,
        plan_name: str | None = None,
    ) -> None:
        subject = f"招生申请环节调整通知：已退回至{target_stage_label}"
        plan_line = f"招生计划：{plan_name}\n" if plan_name else ""
        text_body = (
            f"{student_name}，您好：\n\n"
            "您的招生申请已由平台管理员调整流程节点，请及时登录系统查看最新安排。\n\n"
            f"业务编号：{business_key}\n"
            f"当前退回环节：{target_stage_label}\n"
            f"{plan_line}"
            "如后续需补充材料、重新评审或等待下一步通知，请以系统页面、邮件或电话通知为准。\n\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(
            to_email=email,
            subject=subject,
            text_body=text_body,
            template_code="recruitment_stage_rollback",
            business_key=business_key,
        )

    def send_message(
        self,
        *,
        to_email: str,
        subject: str,
        text_body: str,
        template_code: str | None = None,
        business_key: str | None = None,
        triggered_by: str | None = None,
    ) -> None:
        if not self.enabled():
            logger.info("Skip email delivery because SMTP is disabled or incomplete")
            self._record_delivery(
                channel="email",
                recipient=to_email,
                subject=subject,
                send_status="skipped",
                template_code=template_code,
                business_key=business_key,
                triggered_by=triggered_by,
                failure_reason="SMTP is disabled or incomplete",
            )
            return
        if not to_email:
            logger.info("Skip email delivery because recipient email is empty")
            self._record_delivery(
                channel="email",
                recipient=to_email,
                subject=subject,
                send_status="skipped",
                template_code=template_code,
                business_key=business_key,
                triggered_by=triggered_by,
                failure_reason="Recipient email is empty",
            )
            return

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self._format_from_address()
        message["To"] = to_email
        message.set_content(text_body)

        try:
            self._send_via_smtp(message)
            self._record_delivery(
                channel="email",
                recipient=to_email,
                subject=subject,
                send_status="success",
                template_code=template_code,
                business_key=business_key,
                triggered_by=triggered_by,
            )
        except Exception as exc:
            logger.warning("Send email failed: %s", exc)
            self._record_delivery(
                channel="email",
                recipient=to_email,
                subject=subject,
                send_status="failed",
                template_code=template_code,
                business_key=business_key,
                triggered_by=triggered_by,
                failure_reason=str(exc),
            )

    def _dispatch_async(self, func, *args: str) -> None:
        try:
            thread = Thread(target=func, args=args, daemon=True)
            thread.start()
        except Exception as exc:
            logger.warning("Dispatch async email task failed: %s", exc)
            func(*args)

    def _record_delivery(
        self,
        *,
        channel: str,
        recipient: str,
        subject: str,
        send_status: str,
        template_code: str | None = None,
        business_key: str | None = None,
        triggered_by: str | None = None,
        failure_reason: str | None = None,
    ) -> None:
        if self._log_delivery is None:
            return
        try:
            self._log_delivery(
                channel=channel,
                recipient=recipient,
                subject=subject,
                send_status=send_status,
                template_code=template_code,
                business_key=business_key,
                triggered_by=triggered_by,
                failure_reason=failure_reason,
            )
        except Exception as exc:
            logger.warning("Record notification delivery log failed: %s", exc)

    def _format_from_address(self) -> str:
        from_name = self._settings.smtp_from_name.strip()
        from_email = self._settings.smtp_from_email.strip()
        if from_name:
            return f"{from_name} <{from_email}>"
        return from_email

    def _send_via_smtp(self, message: EmailMessage) -> None:
        timeout = self._settings.smtp_timeout_seconds
        if self._settings.smtp_use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self._settings.smtp_host, self._settings.smtp_port, timeout=timeout, context=context) as server:
                self._login_if_needed(server)
                server.send_message(message)
            return

        with smtplib.SMTP(self._settings.smtp_host, self._settings.smtp_port, timeout=timeout) as server:
            if self._settings.smtp_use_tls:
                context = ssl.create_default_context()
                server.starttls(context=context)
            self._login_if_needed(server)
            server.send_message(message)

    def _login_if_needed(self, server: smtplib.SMTP) -> None:
        username = self._settings.smtp_username.strip()
        if username:
            server.login(username, self._settings.smtp_password)
