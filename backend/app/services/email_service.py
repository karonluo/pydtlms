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
    ) -> None:
        subject = f"招生申请状态更新通知：{application_status}"
        plan_line = f"招生计划：{plan_name}\n" if plan_name else ""
        guidance_map = {
            "资格审核通过": "您的申请已通过资格审核，后续请留意系统中的后续安排。\n",
            "预录取": "您的申请已进入预录取阶段，请关注后续确认通知。\n",
            "同意录取": "您的申请已确认录取，请按后续通知完成相关手续。\n",
            "驳回重填": "您的申请已被驳回重填，请登录系统补充或修改信息后重新提交。\n",
            "不录取": "很遗憾，本次申请未获通过。如需继续申请，请重新登录系统补充并重新提交申报内容。\n",
        }
        guidance_line = guidance_map.get(application_status, "请及时登录系统查看最新进展。\n")
        text_body = (
            f"{student_name}，您好：\n\n"
            "您的招生申请状态已更新，请及时登录系统查看。\n\n"
            f"业务编号：{business_key}\n"
            f"当前状态：{application_status}\n"
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
