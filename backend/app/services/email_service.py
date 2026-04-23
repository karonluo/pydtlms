from __future__ import annotations

import logging
import smtplib
import ssl
from email.message import EmailMessage

from app.core.config import Settings, settings


logger = logging.getLogger(__name__)


class NotificationEmailService:
    def __init__(self, settings_obj: Settings | None = None) -> None:
        self._settings = settings_obj or settings

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
            "您已成功注册博士生生命周期管理系统申请系统账号。"
            "后续可使用注册手机号或邮箱登录系统并继续完善报名信息。\n\n"
            f"登录账号：{email}\n\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(to_email=email, subject=subject, text_body=text_body)

    def send_portal_registration_verification_code(self, email: str, verification_code: str) -> None:
        subject = "申请系统邮箱验证码"
        text_body = (
            "您好：\n\n"
            "您正在进行申请系统注册。\n"
            f"本次邮箱验证码为：{verification_code}\n"
            "验证码 10 分钟内有效，请勿泄露给他人。\n\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(to_email=email, subject=subject, text_body=text_body)

    def send_portal_password_reset_success(self, full_name: str, email: str, account: str) -> None:
        subject = "申请系统密码重置成功通知"
        text_body = (
            f"{full_name}，您好：\n\n"
            "您的申请系统密码已成功重置。"
            "请尽快使用新密码重新登录，并妥善保管账号信息。\n\n"
            f"重置账号：{account}\n\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(to_email=email, subject=subject, text_body=text_body)

    def send_portal_admin_password_reset(self, full_name: str, email: str, temporary_password: str) -> None:
        subject = "申请系统密码重置通知"
        text_body = (
            f"{full_name}，您好：\n\n"
            "管理员已为您重置申请系统登录密码，请尽快登录后修改为您自己的密码。\n\n"
            f"临时密码：{temporary_password}\n\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(to_email=email, subject=subject, text_body=text_body)

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
        text_body = (
            f"{student_name}，您好：\n\n"
            "您的招生申请状态已更新，请及时登录系统查看。\n\n"
            f"业务编号：{business_key}\n"
            f"当前状态：{application_status}\n"
            f"{plan_line}\n"
            "此邮件为系统自动发送，请勿直接回复。"
        )
        self.send_message(to_email=email, subject=subject, text_body=text_body)

    def send_message(self, *, to_email: str, subject: str, text_body: str) -> None:
        if not self.enabled():
            logger.info("Skip email delivery because SMTP is disabled or incomplete")
            return
        if not to_email:
            logger.info("Skip email delivery because recipient email is empty")
            return

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = self._format_from_address()
        message["To"] = to_email
        message.set_content(text_body)

        try:
            self._send_via_smtp(message)
        except Exception as exc:
            logger.warning("Send email failed: %s", exc)

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
