from __future__ import annotations

import logging
import time
from email.message import EmailMessage
import smtplib
import ssl

from app.core.config import settings
from app.services.postgres_state_store import PostgresStateStore
from psycopg.rows import dict_row


logger = logging.getLogger(__name__)
query_store = PostgresStateStore()


def _parse_recipient_emails(raw_value: str | None) -> list[str]:
	return [item.strip() for item in str(raw_value or '').split(';') if item.strip()]


def get_initial_screening_confirmation_student_count() -> int:
	"""Return the number of students currently in the initial-screening-confirmation stage."""
	with query_store._connect(settings.postgres_db) as conn:
		conn.row_factory = dict_row
		with conn.cursor() as cur:
			cur.execute(
				"""
				select count(*) as total
				from dtlms_recruitment_applications
				where application_status = 'initial_screening_confirmation'
				"""
			)
			row = cur.fetchone()
			return int(row.get('total') if row else 0)


def build_initial_screening_confirmation_email_body(student_count: int) -> tuple[str, str]:
	subject = '初筛确认阶段学生统计通知'
	body = (
		'各位老师好，\n\n'
		f'当前已进入“初筛确认”阶段的学生共有：{student_count} 人。\n\n'
		'统计口径：\n'
		'来源于系统“仪表盘”-“学生报名状态统计”-“等待初筛确认”。\n\n'
		'如需查看详情，请登录系统进一步确认。\n\n'
		'谢谢。'
	)
	return subject, body


def _format_from_address() -> str:
	from_name = str(settings.smtp_from_name or '').strip()
	from_email = str(settings.smtp_from_email or '').strip()
	if from_name:
		return f'{from_name} <{from_email}>'
	return from_email


def _send_message_via_smtp(*, to_email: str, subject: str, text_body: str) -> None:
	message = EmailMessage()
	message['Subject'] = subject
	message['From'] = _format_from_address()
	message['To'] = to_email
	message.set_content(text_body)
	timeout = settings.smtp_timeout_seconds
	if settings.smtp_use_ssl:
		context = ssl.create_default_context()
		with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=timeout, context=context) as server:
			username = str(settings.smtp_username or '').strip()
			if username:
				server.login(username, settings.smtp_password)
			server.send_message(message)
		return
	with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=timeout) as server:
		if settings.smtp_use_tls:
			context = ssl.create_default_context()
			server.starttls(context=context)
		username = str(settings.smtp_username or '').strip()
		if username:
			server.login(username, settings.smtp_password)
		server.send_message(message)


def send_initial_screening_confirmation_statistics() -> dict[str, object]:
	"""Send the initial-screening-confirmation statistics email to configured recipients."""
	if not settings.initial_screening_confirmation_smtp_enabled:
		logger.info('Skip initial screening confirmation notification because dedicated SMTP switch is disabled')
		return {'status': 'skipped', 'reason': 'dedicated SMTP switch is disabled'}
	if not settings.smtp_host or not settings.smtp_port or not settings.smtp_from_email:
		logger.warning('Skip initial screening confirmation notification because SMTP settings are incomplete')
		return {'status': 'skipped', 'reason': 'SMTP settings are incomplete'}
	recipients = _parse_recipient_emails(settings.initial_screening_confirmation_email_list)
	student_count = get_initial_screening_confirmation_student_count()
	subject, body = build_initial_screening_confirmation_email_body(student_count)

	if not recipients:
		logger.warning('Skip initial screening confirmation notification because recipient list is empty')
		return {'status': 'skipped', 'reason': 'recipient list is empty', 'total': student_count}

	for recipient in recipients:
		_send_message_via_smtp(to_email=recipient, subject=subject, text_body=body)

	return {
		'status': 'sent',
		'total': student_count,
		'recipient_count': len(recipients),
	}


def run_initial_screening_confirmation_scheduler_once() -> dict[str, object]:
	"""Run the notification job once; intended to be called by a periodic scheduler."""
	return send_initial_screening_confirmation_statistics()


def sleep_initial_screening_confirmation_timeout() -> None:
	"""Sleep for the configured timeout interval."""
	time.sleep(max(int(settings.initial_screening_confirmation_timeout_second or 0), 1))
