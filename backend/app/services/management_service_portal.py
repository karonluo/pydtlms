from __future__ import annotations

from .management_service_shared import *


class RuntimeManagementStorePortalMixin:
    @staticmethod
    def _portal_application_summary_form_status(submitted_at: str | None, application_status: str | None) -> str:
        normalized_status = str(application_status or "").strip()
        if normalized_status == "驳回重填":
            return "驳回重填"
        if normalized_status == "未提交":
            return "未提交报名"
        if normalized_status == "待中心考核-第一志愿":
            return "第一志愿考核"
        if normalized_status == "待中心考核-第二志愿":
            return "第二志愿考核"
        if normalized_status in {"结果公布", "报名终止", "预录取"}:
            return "已结束报名流程"
        if submitted_at:
            return "已填写报名"
        return "未提交报名"

    def _build_portal_workflow_progress_summary(self, submitted_at: str | None, application_status: str | None) -> PortalWorkflowProgressSummary:
        normalized_status = str(application_status or "").strip()
        application_form_status = self._portal_application_summary_form_status(submitted_at, normalized_status or None)
        stage_labels = [
            ("online_application", "在线申请"),
            ("material_review", "资料审核"),
            ("background_review", "背景评估"),
            ("center_assessment", "中心考核"),
            ("result_publish", "结果公布"),
            ("pre_admission", "预录取"),
        ]
        stages = [PortalWorkflowStageItem(key=key, label=label) for key, label in stage_labels]

        if normalized_status == "驳回重填":
            stages[0].status = "returned"
            stages[0].description = "申请已被驳回，请完善后重新提交"
            stages[1].status = "returned"
            return PortalWorkflowProgressSummary(
                current_stage_key="online_application",
                current_stage_label="在线申请",
                application_form_status=application_form_status,
                recruitment_application_status="驳回重填",
                stages=stages,
            )

        if not submitted_at and not normalized_status:
            stages[0].status = "current"
            stages[0].description = "请先完成在线申请并提交报名"
            return PortalWorkflowProgressSummary(
                current_stage_key="online_application",
                current_stage_label="在线申请",
                application_form_status=application_form_status,
                recruitment_application_status="未提交",
                stages=stages,
            )

        current_stage_key = "material_review"
        current_stage_label = "资料审核"
        result_label: str | None = None

        if normalized_status in {"报名已提交", "待审核", ""}:
            stages[0].status = "completed"
            stages[1].status = "current"
            stages[1].description = "已提交报名，等待审核"
            current_stage_key = "material_review"
            current_stage_label = "资料审核"
            normalized_status = normalized_status or "待审核"
        elif normalized_status in {"资格审核通过", "材料评分中", "待背景评估"}:
            stages[0].status = "completed"
            stages[1].status = "completed"
            stages[2].status = "current"
            stages[2].description = "资料审核已通过，等待背景评估"
            current_stage_key = "background_review"
            current_stage_label = "背景评估"
            normalized_status = "待背景评估"
        elif normalized_status in {"面试待安排", "面试完成", "待中心考核", "待中心考核-第一志愿", "待中心考核-第二志愿"}:
            stages[0].status = "completed"
            stages[1].status = "completed"
            stages[2].status = "completed"
            stages[3].status = "current"
            current_stage_key = "center_assessment"
            current_stage_label = "中心考核"
            if normalized_status == "待中心考核-第二志愿":
                stages[3].description = "当前进入第二志愿考核阶段"
            else:
                stages[3].description = "等待研究中心完成考核结果处理"
                normalized_status = "待中心考核"
        elif normalized_status in {"结果公布"}:
            stages[0].status = "completed"
            stages[1].status = "completed"
            stages[2].status = "completed"
            stages[3].status = "completed"
            stages[4].status = "current"
            stages[4].description = "结果待发布，请留意门户与邮件通知"
            current_stage_key = "result_publish"
            current_stage_label = "结果公布"
        elif normalized_status in {"预录取", "同意录取"}:
            stages[0].status = "completed"
            stages[1].status = "completed"
            stages[2].status = "completed"
            stages[3].status = "completed"
            stages[4].status = "completed"
            stages[5].status = "current"
            stages[5].description = "结果已发布，请按要求完成预录取确认"
            current_stage_key = "pre_admission"
            current_stage_label = "预录取"
            normalized_status = "预录取"
            result_label = "已进入预录取"
        elif normalized_status in {"不录取", "报名终止"}:
            stages[0].status = "completed"
            stages[1].status = "completed"
            stages[2].status = "completed"
            stages[3].status = "terminated"
            stages[4].status = "current"
            stages[4].description = "当前报名流程已结束"
            current_stage_key = "result_publish"
            current_stage_label = "结果公布"
            normalized_status = "报名终止"
            result_label = "不合格"
        else:
            stages[0].status = "completed"
            stages[1].status = "current"
            stages[1].description = "当前状态待系统进一步归类"

        return PortalWorkflowProgressSummary(
            current_stage_key=current_stage_key,
            current_stage_label=current_stage_label,
            application_form_status=application_form_status,
            recruitment_application_status=normalized_status or None,
            result_label=result_label,
            stages=stages,
        )

    def _get_latest_portal_application_status(self, student: dict[str, Any]) -> str | None:
        student_id = int(student.get("id") or 0)
        if student_id <= 0:
            return None
        selected_plan_id = student.get("selected_plan_id")
        applications = [
            application for application in self._list("recruitment_applications")
            if int(application.get("portal_student_id") or 0) == student_id
        ]
        if not applications:
            return None

        def _sort_key(application: dict[str, Any]) -> tuple[int, str, int]:
            same_plan = 0
            if selected_plan_id is not None and int(application.get("plan_id") or 0) == int(selected_plan_id):
                same_plan = 1
            timestamp = str(application.get("applied_at") or application.get("created_at") or "")
            return (same_plan, timestamp, int(application.get("id") or 0))

        latest_application = max(applications, key=_sort_key)
        return str(latest_application.get("application_status") or "").strip() or None

    @staticmethod
    def _portal_plan_sort_key(item: dict[str, Any]) -> tuple[int, int, int]:
        year_text = str(item.get("academic_year") or "").strip()
        try:
            academic_year = int(year_text)
        except ValueError:
            academic_year = 0
        semester_order = {"春": 1, "夏": 2, "秋": 3, "冬": 4}.get(str(item.get("semester") or "").strip(), 0)
        return academic_year, semester_order, int(item.get("id") or 0)

    def _get_latest_recruitment_plan_id(self) -> int | None:
        plans = list(self._list("recruitment_plans"))
        if not plans:
            return None
        latest_plan = max(plans, key=self._portal_plan_sort_key)
        plan_id = int(latest_plan.get("id") or 0)
        return plan_id if plan_id > 0 else None

    def _build_portal_student_record(self, item: dict[str, Any]) -> PortalStudentRecord:
        normalized = dict(item)
        normalized["account_status"] = self._normalize_portal_account_status(normalized.get("account_status"))
        normalized["submitted_at"] = self._normalize_portal_timestamp(normalized.get("submitted_at"))
        application_status = str(normalized.get("recruitment_application_status") or normalized.get("application_status") or "").strip() or None
        if application_status is None:
            application_status = self._get_latest_portal_application_status(normalized)
        normalized["recruitment_application_status"] = application_status
        normalized["application_form_status"] = self._portal_application_summary_form_status(normalized.get("submitted_at"), application_status)
        normalized["workflow_progress"] = self._build_portal_workflow_progress_summary(normalized.get("submitted_at"), application_status)
        profile = normalized.get("profile")
        if isinstance(profile, dict):
            profile_payload = dict(profile)
            try:
                profile_payload["emergency_contact_phone"] = validate_optional_phone_number(
                    profile_payload.get("emergency_contact_phone"),
                    "紧急联系人手机",
                )
            except ValueError:
                profile_payload["emergency_contact_phone"] = None
            normalized["profile"] = profile_payload
        draft = normalized.get("application_draft")
        if isinstance(draft, dict):
            draft_payload = dict(draft)
            draft_payload["submitted_at"] = self._normalize_portal_timestamp(draft_payload.get("submitted_at"))
            normalized["application_draft"] = draft_payload
        if not normalized.get("business_key") and not normalized.get("candidate_no"):
            student_id = normalized.get("id")
            selected_plan_id = normalized.get("selected_plan_id")
            applications = [
                application for application in self._list("recruitment_applications")
                if int(application.get("portal_student_id") or 0) == int(student_id or 0)
            ]
            if applications:
                def _sort_key(application: dict[str, Any]) -> tuple[int, str, int]:
                    same_plan = 0
                    if selected_plan_id is not None and int(application.get("plan_id") or 0) == int(selected_plan_id):
                        same_plan = 1
                    timestamp = str(application.get("applied_at") or application.get("created_at") or "")
                    return (same_plan, timestamp, int(application.get("id") or 0))

                latest_application = max(applications, key=_sort_key)
                normalized["business_key"] = latest_application.get("business_key")
                normalized["candidate_no"] = latest_application.get("candidate_no")
        return PortalStudentRecord(**normalized)

    @staticmethod
    def _normalize_portal_timestamp(value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(value, date):
            return value.isoformat()
        text = str(value).strip()
        return text or None

    def _refresh_portal_student_from_postgres(self, student_id: int) -> dict[str, Any] | None:
        postgres_item = self._postgres_store.get_portal_student_detail(student_id)
        if postgres_item is None:
            return None

        portal_students = self._list("portal_students")
        existing = next((item for item in portal_students if int(item.get("id") or 0) == int(student_id)), None)
        if existing is not None:
            password_hash = existing.get("password_hash")
            existing.clear()
            existing.update(postgres_item)
            if existing.get("password_hash") in {None, ""} and password_hash:
                existing["password_hash"] = password_hash
            return existing

        portal_students.insert(0, dict(postgres_item))
        return portal_students[0]

    @staticmethod
    def _generate_portal_temporary_password(length: int = 10) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def _normalize_portal_account_status(value: Any) -> str:
        text = str(value or "").strip()
        if text in {"已注销", "停用"}:
            return "停用"
        return "启用"

    def _find_existing_recruitment_application_for_portal_student(
        self,
        student: dict[str, Any],
        *,
        plan_id: int | None = None,
    ) -> dict[str, Any] | None:
        student_id = int(student.get("id") or 0)
        phone_number = str(student.get("phone_number") or "").strip()
        email = str(student.get("email") or "").strip().lower()
        matches: list[dict[str, Any]] = []
        for item in self._list("recruitment_applications"):
            if plan_id is not None and int(item.get("plan_id") or 0) != int(plan_id):
                continue
            item_student_id = int(item.get("portal_student_id") or 0)
            item_phone = str(item.get("phone_number") or "").strip()
            item_email = str(item.get("email") or "").strip().lower()
            if item_student_id > 0 and student_id > 0 and item_student_id == student_id:
                matches.append(item)
                continue
            if phone_number and item_phone == phone_number and email and item_email == email:
                matches.append(item)

        if not matches:
            return None

        return max(
            matches,
            key=lambda item: (
                str(item.get("applied_at") or item.get("created_at") or ""),
                int(item.get("id") or 0),
            ),
        )

    def _build_portal_profile_payload(self, payload: Any) -> dict[str, Any] | None:
        profile = payload.profile.model_dump(mode="python") if payload.profile is not None else {}
        fallback_profile = {
            "gender": payload.gender,
            "birth_date": payload.birth_date,
            "ethnic_group": payload.ethnic_group,
            "native_place": payload.native_place,
            "political_status": payload.political_status,
            "marital_status": payload.marital_status,
            "religious_belief": payload.religious_belief,
            "id_type": payload.id_type,
            "mailing_address": payload.mailing_address,
        }
        for key, value in fallback_profile.items():
            profile.setdefault(key, value)
        return profile or None

    def _build_portal_application_draft_payload(
        self,
        payload: Any,
        selected_team_id: int | None,
        selected_team_name: str | None,
        selected_advisor_user_id: int | None,
        advisor_name: str | None,
        submitted_at: str | None,
    ) -> dict[str, Any]:
        preferences: list[dict[str, Any]] = []
        for item in sorted(payload.preferences, key=lambda preference: preference.preference_order):
            resolved_advisor = self._resolve_portal_advisor_selection(
                item.advisor_user_id,
                item.advisor_name,
                require_advisor=not bool(item.is_optional),
            )
            if resolved_advisor["advisor_user_id"] is None and not resolved_advisor["advisor_name"]:
                continue
            preferences.append(
                {
                    "preference_order": item.preference_order,
                    "team_id": item.team_id,
                    "research_center_name": str(item.research_center_name or "").strip() or None,
                    "advisor_user_id": resolved_advisor["advisor_user_id"],
                    "advisor_name": resolved_advisor["advisor_name"],
                    "is_optional": item.is_optional,
                }
            )
        if not preferences and (selected_advisor_user_id is not None or advisor_name):
            preferences = [
                {
                    "preference_order": 1,
                    "team_id": selected_team_id,
                    "research_center_name": selected_team_name,
                    "advisor_user_id": selected_advisor_user_id,
                    "advisor_name": advisor_name,
                    "is_optional": False,
                }
            ]
        personal_statement = payload.personal_statement.model_dump(mode="python") if payload.personal_statement is not None else {}
        if payload.personal_statement_text and not personal_statement.get("personal_statement_text"):
            personal_statement["personal_statement_text"] = payload.personal_statement_text
        declaration = payload.declaration.model_dump(mode="python") if payload.declaration is not None else {}
        declaration.setdefault("has_read_declaration", bool(payload.signed_agreement))
        return {
            "selected_plan_id": payload.plan_id,
            "selected_team_id": selected_team_id,
            "selected_advisor_user_id": selected_advisor_user_id,
            "source_channel": payload.source_channel,
            "source_channel_other": payload.source_channel_other,
            "preferences": preferences,
            "education_experiences": [item.model_dump() for item in payload.education_experiences],
            "practice_experiences": [item.model_dump() for item in payload.practice_experiences],
            "english_proficiencies": [item.model_dump() for item in payload.english_proficiencies],
            "family_members": [item.model_dump() for item in payload.family_members],
            "achievement_records": [item.model_dump() for item in payload.achievement_records],
            "personal_statement": personal_statement,
            "declaration": declaration,
            "submitted_at": submitted_at,
        }

    def _build_portal_plan_record(self, item: dict[str, Any]) -> PortalPlanRecord:
        plan = self._build_recruit_plan_record(item)
        return PortalPlanRecord(
            id=plan.id,
            plan_name=plan.plan_name,
            academic_term=plan.academic_term,
            brochure_image_url=plan.brochure_image_url,
            summary=plan.plan_description,
        )

    def _build_portal_team_record(self, item: dict[str, Any]) -> PortalTeamRecord:
        team = self._build_center_record(item)
        return PortalTeamRecord(
            id=team.id,
            team_name=team.center_name,
            lead_user_id=team.director_id,
            lead_advisor_name=team.director_name,
            advisor_names=team.advisor_names,
            advisor_ids=team.advisor_ids,
            advisor_relation_ids=team.advisor_relation_ids,
            department_name=str(item.get("department_name") or ""),
            discipline_name=str(item.get("discipline_name") or ""),
            research_directions=[str(value).strip() for value in item.get("research_directions") or [] if str(value).strip()],
            description=item.get("description"),
        )

    @staticmethod
    def _portal_registration_email_cache_token(email: str) -> str:
        normalized = str(email or "").strip().lower()
        return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:24]

    def _portal_registration_email_code_key(self, email: str) -> str:
        return build_cache_key("portal", "register", "email-code", self._portal_registration_email_cache_token(email))

    def _portal_registration_email_cooldown_key(self, email: str) -> str:
        return build_cache_key("portal", "register", "email-cooldown", self._portal_registration_email_cache_token(email))

    def _portal_login_email_code_key(self, email: str) -> str:
        return build_cache_key("portal", "login", "email-code", self._portal_registration_email_cache_token(email))

    def _portal_login_email_cooldown_key(self, email: str) -> str:
        return build_cache_key("portal", "login", "email-cooldown", self._portal_registration_email_cache_token(email))

    def send_portal_registration_email_code(self, email: str) -> PortalRegistrationEmailCodeResponse:
        normalized_email = str(email or "").strip()
        with self._lock:
            if any(item.get("email") == normalized_email for item in self._list("portal_students")):
                raise ValueError("该邮箱已注册，请直接登录")

        if not self._email_service.enabled():
            raise RuntimeError("邮件服务未启用，暂无法发送邮箱验证码")

        try:
            client = self._get_cache_client()
            cooldown_key = self._portal_registration_email_cooldown_key(normalized_email)
            if client.exists(cooldown_key):
                remaining_seconds = int(client.ttl(cooldown_key) or 0)
                if remaining_seconds <= 0:
                    remaining_seconds = PORTAL_REGISTRATION_EMAIL_CODE_COOLDOWN_SECONDS
                raise ValueError(f"验证码已发送，请{remaining_seconds}秒后重试")

            verification_code = "".join(
                secrets.choice(string.digits) for _ in range(PORTAL_REGISTRATION_EMAIL_CODE_LENGTH)
            )
            client.set(
                self._portal_registration_email_code_key(normalized_email),
                verification_code,
                ex=PORTAL_REGISTRATION_EMAIL_CODE_EXPIRES_SECONDS,
            )
            client.set(cooldown_key, "1", ex=PORTAL_REGISTRATION_EMAIL_CODE_COOLDOWN_SECONDS)
        except ValueError:
            raise
        except Exception as exc:
            raise RuntimeError("验证码服务暂不可用，请稍后再试") from exc

        self._email_service.send_portal_registration_verification_code(normalized_email, verification_code)
        return PortalRegistrationEmailCodeResponse(
            message="邮件验证码已发送，请查收邮箱",
            expires_in_seconds=PORTAL_REGISTRATION_EMAIL_CODE_EXPIRES_SECONDS,
            cooldown_seconds=PORTAL_REGISTRATION_EMAIL_CODE_COOLDOWN_SECONDS,
        )

    def validate_portal_registration_email_code(self, email: str, verification_code: str) -> None:
        normalized_email = str(email or "").strip()
        normalized_code = str(verification_code or "").strip()
        try:
            client = self._get_cache_client()
            cached_code = client.get(self._portal_registration_email_code_key(normalized_email))
        except Exception as exc:
            raise RuntimeError("验证码服务暂不可用，请稍后再试") from exc

        if not isinstance(cached_code, (str, bytes, bytearray)):
            raise ValueError("邮件验证码已过期或不存在，请重新获取")
        if isinstance(cached_code, (bytes, bytearray)):
            cached_text = cached_code.decode("utf-8", errors="ignore").strip()
        else:
            cached_text = cached_code.strip()
        if not cached_text:
            raise ValueError("邮件验证码已过期或不存在，请重新获取")
        if cached_text != normalized_code:
            raise ValueError("邮件验证码不正确")

    def clear_portal_registration_email_code(self, email: str) -> None:
        normalized_email = str(email or "").strip()
        try:
            client = self._get_cache_client()
            client.delete(
                self._portal_registration_email_code_key(normalized_email),
                self._portal_registration_email_cooldown_key(normalized_email),
            )
        except Exception as exc:
            logger.warning("Clear portal registration email code failed: %s", exc)

    def send_portal_login_email_code(self, email: str) -> PortalRegistrationEmailCodeResponse:
        normalized_email = str(email or "").strip()
        with self._lock:
            student = next((item for item in self._list("portal_students") if item.get("email") == normalized_email), None)
            if not student:
                raise ValueError("该邮箱未注册，请先注册")
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，请联系管理员")

        if not self._email_service.enabled():
            raise RuntimeError("邮件服务未启用，暂无法发送邮箱验证码")

        try:
            client = self._get_cache_client()
            cooldown_key = self._portal_login_email_cooldown_key(normalized_email)
            if client.exists(cooldown_key):
                remaining_seconds = int(client.ttl(cooldown_key) or 0)
                if remaining_seconds <= 0:
                    remaining_seconds = PORTAL_REGISTRATION_EMAIL_CODE_COOLDOWN_SECONDS
                raise ValueError(f"验证码已发送，请{remaining_seconds}秒后重试")

            verification_code = "".join(
                secrets.choice(string.digits) for _ in range(PORTAL_REGISTRATION_EMAIL_CODE_LENGTH)
            )
            client.set(
                self._portal_login_email_code_key(normalized_email),
                verification_code,
                ex=PORTAL_REGISTRATION_EMAIL_CODE_EXPIRES_SECONDS,
            )
            client.set(cooldown_key, "1", ex=PORTAL_REGISTRATION_EMAIL_CODE_COOLDOWN_SECONDS)
        except ValueError:
            raise
        except Exception as exc:
            raise RuntimeError("验证码服务暂不可用，请稍后再试") from exc

        self._email_service.send_portal_login_verification_code(normalized_email, verification_code)
        return PortalRegistrationEmailCodeResponse(
            message="登录验证码已发送，请查收邮箱",
            expires_in_seconds=PORTAL_REGISTRATION_EMAIL_CODE_EXPIRES_SECONDS,
            cooldown_seconds=PORTAL_REGISTRATION_EMAIL_CODE_COOLDOWN_SECONDS,
        )

    def validate_portal_login_email_code(self, email: str, verification_code: str) -> None:
        normalized_email = str(email or "").strip()
        normalized_code = str(verification_code or "").strip()
        try:
            client = self._get_cache_client()
            cached_code = client.get(self._portal_login_email_code_key(normalized_email))
        except Exception as exc:
            raise RuntimeError("验证码服务暂不可用，请稍后再试") from exc

        if not isinstance(cached_code, (str, bytes, bytearray)):
            raise ValueError("邮件验证码已过期或不存在，请重新获取")
        if isinstance(cached_code, (bytes, bytearray)):
            cached_text = cached_code.decode("utf-8", errors="ignore").strip()
        else:
            cached_text = cached_code.strip()
        if not cached_text:
            raise ValueError("邮件验证码已过期或不存在，请重新获取")
        if cached_text != normalized_code:
            raise ValueError("邮件验证码不正确")

    def clear_portal_login_email_code(self, email: str) -> None:
        normalized_email = str(email or "").strip()
        try:
            client = self._get_cache_client()
            client.delete(
                self._portal_login_email_code_key(normalized_email),
                self._portal_login_email_cooldown_key(normalized_email),
            )
        except Exception as exc:
            logger.warning("Clear portal login email code failed: %s", exc)

    def register_portal_student(self, payload: PortalRegistrationRequest) -> PortalRegistrationResponse:
        request_started_at = perf_counter()
        with self._lock:
            now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            latest_plan_id = self._get_latest_recruitment_plan_id()
            if any(item.get("phone_number") == payload.phone_number for item in self._list("portal_students")):
                raise ValueError("该手机号已注册，请直接登录")
            if any(item.get("email") == payload.email for item in self._list("portal_students")):
                raise ValueError("该邮箱已注册，请直接登录")
            if any(item.get("id_number") == payload.id_number for item in self._list("portal_students")):
                raise ValueError("该身份证号已注册，请使用找回密码")

            item = payload.model_dump()
            password = item.pop("password")
            password_hash_started_at = perf_counter()
            password_hash = PASSWORD_CONTEXT.hash(password)
            password_hash_elapsed_ms = round((perf_counter() - password_hash_started_at) * 1000, 2)
            item.update(
                {
                    "id": self._next_id("portal_students"),
                    "account_status": "启用",
                    "password_hash": password_hash,
                    "gender": None,
                    "birth_date": None,
                    "ethnic_group": None,
                    "native_place": None,
                    "marital_status": None,
                    "religious_belief": None,
                    "id_type": "居民身份证",
                    "mailing_address": None,
                    "graduation_school": None,
                    "highest_degree": None,
                    "intended_field": None,
                    "political_status": None,
                    "english_level": None,
                    "family_info": None,
                    "education_experience": None,
                    "practice_experience": None,
                    "personal_profile": None,
                    "recommendation_notes": None,
                    "personal_statement_text": None,
                    "signed_agreement": False,
                    "selected_plan_id": latest_plan_id,
                    "selected_team_name": None,
                    "selected_advisor_name": None,
                    "self_evaluation": None,
                    "submitted_at": None,
                    "created_at": now_text,
                    "updated_at": now_text,
                }
            )
            self._list("portal_students").insert(0, item)
            persist_started_at = perf_counter()
            try:
                self._persist_portal_student_change(item, None, update_student_counter=True)
                persist_mode = "incremental"
                persist_elapsed_ms = round((perf_counter() - persist_started_at) * 1000, 2)
            except Exception as exc:
                logger.warning("Portal register incremental persistence failed, fallback to full save: %s", exc, exc_info=True)
                self._save()
                persist_mode = "full_save_fallback"
                persist_elapsed_ms = round((perf_counter() - persist_started_at) * 1000, 2)
            response = PortalRegistrationResponse(message="注册成功，请使用手机号或邮箱登录", student=self._build_portal_student_record(item))

        total_elapsed_ms = round((perf_counter() - request_started_at) * 1000, 2)
        logger.info(
            "Portal register completed: student_id=%s mode=%s hash_ms=%s persist_ms=%s total_ms=%s",
            item["id"],
            persist_mode,
            password_hash_elapsed_ms,
            persist_elapsed_ms,
            total_elapsed_ms,
        )

        if self._email_service.enabled():
            self._email_service.send_portal_registration_success_async(item["full_name"], item["email"])
        return response

    def login_portal_student(self, payload: PortalLoginRequest) -> PortalStudentRecord:
        account = payload.account.strip()
        with self._lock:
            student = next(
                (
                    item for item in self._list("portal_students")
                    if item.get("phone_number") == account or item.get("email") == account
                ),
                None,
            )
            if not student:
                raise ValueError("账号不存在")
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，请联系管理员")
            password_hash = student.get("password_hash")
            if not password_hash or not PASSWORD_CONTEXT.verify(payload.password, password_hash):
                raise ValueError("账号或密码错误")
            student = self._refresh_portal_student_from_postgres(int(student["id"])) or student
            return self._build_portal_student_record(student)

    def login_portal_student_by_email_code(self, email: str, verification_code: str) -> PortalStudentRecord:
        normalized_email = str(email or "").strip()
        self.validate_portal_login_email_code(normalized_email, verification_code)

        with self._lock:
            student = next((item for item in self._list("portal_students") if item.get("email") == normalized_email), None)
            if not student:
                raise ValueError("账号不存在")
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，请联系管理员")
            student = self._refresh_portal_student_from_postgres(int(student["id"])) or student

        self.clear_portal_login_email_code(normalized_email)
        return self._build_portal_student_record(student)

    def reset_portal_student_password(self, payload: PortalPasswordResetRequest) -> None:
        account = payload.account.strip()
        id_number = payload.id_number.strip()
        with self._lock:
            student = next(
                (
                    item for item in self._list("portal_students")
                    if item.get("phone_number") == account or item.get("email") == account
                ),
                None,
            )
            if not student:
                raise ValueError("账号不存在")
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，请联系管理员")
            if str(student.get("id_number") or "").strip() != id_number:
                raise ValueError("身份证号校验失败")
            student["password_hash"] = PASSWORD_CONTEXT.hash(payload.new_password)
            student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_log = self._record_operation(
                "学生门户",
                "找回密码",
                str(student["id"]),
                "重置密码",
                f'学生 {student["full_name"]} 重置门户密码',
                operator_username=student["phone_number"],
            )
            try:
                self._postgres_store.update_runtime_portal_student(int(student["id"]), student)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

        if self._email_service.enabled():
            self._email_service.send_portal_password_reset_success(student["full_name"], student["email"], account)

    def change_portal_student_password(self, student_id: int, payload: PortalPasswordChangeRequest) -> None:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，无法修改密码")
            password_hash = student.get("password_hash")
            if not password_hash or not PASSWORD_CONTEXT.verify(payload.current_password, password_hash):
                raise ValueError("当前密码不正确")
            student["password_hash"] = PASSWORD_CONTEXT.hash(payload.new_password)
            student["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_log = self._record_operation(
                "学生门户",
                "个人空间",
                str(student_id),
                "修改密码",
                f'学生 {student["full_name"]} 在个人空间修改密码',
                operator_username=student["phone_number"],
            )
            try:
                self._postgres_store.update_runtime_portal_student(int(student_id), student)
                self._postgres_store.update_runtime_counter("operation_logs", int(self._counters.get("operation_logs", 0)))
                self._postgres_store.insert_runtime_operation_log(operation_log)
            except Exception:
                self._save()

    def get_portal_student(self, student_id: int) -> PortalStudentRecord:
        try:
            _, item = self._find_required("portal_students", student_id)
            item = self._refresh_portal_student_from_postgres(student_id) or item
            return self._build_portal_student_record(item)
        except KeyError:
            postgres_item = self._postgres_store.get_portal_student_detail(student_id)
            if postgres_item is not None:
                return self._build_portal_student_record(postgres_item)
            raise

    def get_public_recruitment_plans(self) -> PortalPlanListResponse:
        source_items = sorted(self._list("recruitment_plans"), key=self._portal_plan_sort_key, reverse=True)
        items = [self._build_portal_plan_record(item) for item in source_items]
        return PortalPlanListResponse(items=items)

    def get_public_teams(self) -> PortalTeamListResponse:
        source_items = self._load_teams_from_postgres()
        if not source_items:
            source_items = [
                item
                for item in self._list("teams")
                if not str(item.get("team_code") or "").strip().startswith("TEAM-AUTO-")
            ]

        items = [self._build_portal_team_record(item) for item in source_items if item.get("status") != "停用"]
        return PortalTeamListResponse(items=items)

    def save_portal_application_draft(self, student_id: int, payload: PortalApplicationDraftUpsert) -> PortalStudentRecord:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            student = self._refresh_portal_student_from_postgres(student_id) or student
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，无法保存草稿")
            if student.get("submitted_at"):
                raise ValueError("报名申请已提交，当前仅支持只读浏览，不能再修改信息")

            selected_team_id = payload.selected_team_id
            selected_team_name = payload.selected_team_name
            selected_advisor_user_id = payload.selected_advisor_user_id
            advisor_name = payload.selected_advisor_name
            resolved_selection = self._resolve_portal_advisor_selection(
                selected_advisor_user_id,
                advisor_name,
                require_advisor=False,
            )
            selected_advisor_user_id = resolved_selection["advisor_user_id"]
            advisor_name = resolved_selection["advisor_name"]

            now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            profile_payload = self._build_portal_profile_payload(payload)
            application_draft = self._build_portal_application_draft_payload(
                payload,
                selected_team_id,
                selected_team_name,
                selected_advisor_user_id,
                advisor_name,
                student.get("submitted_at"),
            )

            student.update(
                {
                    "gender": payload.gender,
                    "birth_date": payload.birth_date,
                    "ethnic_group": payload.ethnic_group,
                    "native_place": payload.native_place,
                    "marital_status": payload.marital_status,
                    "religious_belief": payload.religious_belief,
                    "id_type": payload.id_type,
                    "mailing_address": payload.mailing_address,
                    "graduation_school": payload.graduation_school,
                    "highest_degree": payload.highest_degree,
                    "intended_field": payload.intended_field,
                    "political_status": payload.political_status,
                    "english_level": payload.english_level,
                    "family_info": payload.family_info,
                    "education_experience": payload.education_experience,
                    "practice_experience": payload.practice_experience,
                    "personal_profile": payload.personal_profile,
                    "recommendation_notes": payload.recommendation_notes,
                    "personal_statement_text": payload.personal_statement_text,
                    "signed_agreement": payload.signed_agreement,
                    "selected_plan_id": payload.plan_id or student.get("selected_plan_id"),
                    "selected_team_id": selected_team_id,
                    "selected_team_name": selected_team_name,
                    "selected_advisor_user_id": selected_advisor_user_id,
                    "selected_advisor_name": advisor_name,
                    "self_evaluation": payload.self_evaluation,
                    "updated_at": now_text,
                    "profile": profile_payload,
                    "application_draft": application_draft,
                }
            )
            try:
                self._persist_portal_student_change(student, None)
            except Exception:
                self._save()
            return self._build_portal_student_record(student)

    def submit_portal_application(self, student_id: int, payload: PortalApplicationUpsert) -> PortalApplicationSubmissionResponse:
        with self._lock:
            _, student = self._find_required("portal_students", student_id)
            student = self._refresh_portal_student_from_postgres(student_id) or student
            if self._normalize_portal_account_status(student.get("account_status")) != "启用":
                raise ValueError("账号已停用，无法提交报名")
            latest_application = self._find_existing_recruitment_application_for_portal_student(student, plan_id=payload.plan_id)
            latest_application_status = str((latest_application or {}).get("application_status") or "").strip()
            resubmittable_latest_application = latest_application is not None and latest_application_status in PORTAL_RESUBMITTABLE_APPLICATION_STATUSES
            if student.get("submitted_at") and not resubmittable_latest_application:
                raise ValueError("报名申请已提交，当前仅支持只读浏览，不能再修改信息")
            if resubmittable_latest_application and student.get("submitted_at"):
                student["submitted_at"] = None
            _, plan = self._find_required("recruitment_plans", payload.plan_id)
            selected_team_id = payload.selected_team_id
            selected_team_name = payload.selected_team_name
            graduation_school = payload.graduation_school
            if not graduation_school:
                raise ValueError("缺少毕业院校/就读学校信息")
            highest_degree = payload.highest_degree
            if not highest_degree:
                raise ValueError("缺少最高学历/教育阶段信息")
            resolved_selection = self._resolve_portal_advisor_selection(
                payload.selected_advisor_user_id,
                payload.selected_advisor_name,
            )
            selected_advisor_user_id = resolved_selection["advisor_user_id"]
            advisor_name = resolved_selection["advisor_name"]
            intended_field = payload.intended_field or advisor_name
            submitted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            profile_payload = self._build_portal_profile_payload(payload)
            application_draft = self._build_portal_application_draft_payload(
                payload,
                selected_team_id,
                selected_team_name,
                selected_advisor_user_id,
                advisor_name,
                submitted_at,
            )
            preference_advisors = [item.get("advisor_name") for item in application_draft.get("preferences", []) if item.get("advisor_name")]
            second_choice = preference_advisors[1] if len(preference_advisors) > 1 else None
            second_choice_team_id = None

            student.update(
                {
                    "gender": payload.gender,
                    "birth_date": payload.birth_date,
                    "ethnic_group": payload.ethnic_group,
                    "native_place": payload.native_place,
                    "marital_status": payload.marital_status,
                    "religious_belief": payload.religious_belief,
                    "id_type": payload.id_type,
                    "mailing_address": payload.mailing_address,
                    "graduation_school": graduation_school,
                    "highest_degree": highest_degree,
                    "intended_field": payload.intended_field,
                    "political_status": payload.political_status,
                    "english_level": payload.english_level,
                    "family_info": payload.family_info,
                    "education_experience": payload.education_experience,
                    "practice_experience": payload.practice_experience,
                    "personal_profile": payload.personal_profile,
                    "recommendation_notes": payload.recommendation_notes,
                    "personal_statement_text": payload.personal_statement_text,
                    "signed_agreement": payload.signed_agreement,
                    "selected_plan_id": payload.plan_id,
                    "selected_team_id": selected_team_id,
                    "selected_team_name": selected_team_name,
                    "selected_advisor_user_id": selected_advisor_user_id,
                    "selected_advisor_name": advisor_name,
                    "self_evaluation": payload.self_evaluation,
                    "submitted_at": submitted_at,
                    "updated_at": submitted_at,
                    "profile": profile_payload,
                    "application_draft": application_draft,
                }
            )

            existing_application = self._find_existing_recruitment_application_for_portal_student(student, plan_id=payload.plan_id)
            created_application = False
            created_workflow_task = False
            if existing_application:
                previous_application_status = str(existing_application.get("application_status") or "").strip()
                resubmitting_rejected_application = previous_application_status in PORTAL_RESUBMITTABLE_APPLICATION_STATUSES
                existing_application.update(
                    {
                        "student_name": student["full_name"],
                        "gender": payload.gender,
                        "graduation_school": graduation_school,
                        "highest_degree": highest_degree,
                        "intended_field": intended_field,
                        "first_choice_team_id": selected_team_id,
                        "first_choice": advisor_name,
                        "second_choice_team_id": second_choice_team_id,
                        "second_choice": second_choice,
                        "political_status": payload.political_status,
                        "marital_status": payload.marital_status,
                        "religious_belief": payload.religious_belief,
                        "native_place": payload.native_place,
                        "mailing_address": payload.mailing_address,
                        "id_type": payload.id_type,
                        "intended_advisor_user_id": selected_advisor_user_id,
                        "intended_advisor_name": advisor_name,
                        "phone_number": student["phone_number"],
                        "email": student["email"],
                        "id_number": student["id_number"],
                        "family_info": payload.family_info,
                        "education_experience": payload.education_experience,
                        "practice_experience": payload.practice_experience,
                        "personal_statement_text": payload.personal_statement_text,
                        "personal_statement_attachment": (payload.personal_statement.resume_attachment_url if payload.personal_statement else None),
                        "supplementary_profile": payload.personal_profile,
                        "self_evaluation": payload.self_evaluation,
                        "discovery_channel": payload.source_channel_other or payload.source_channel,
                        "source_channel": payload.source_channel,
                        "source_channel_other": payload.source_channel_other,
                        "portal_student_id": student_id,
                        "applied_at": submitted_at,
                        "material_status": "待审核" if resubmitting_rejected_application else existing_application.get("material_status") or "待审核",
                        "application_status": "报名已提交" if resubmitting_rejected_application else previous_application_status,
                    }
                )
                workflow_task, created_workflow_task, task_changed = self._ensure_recruitment_application_workflow_task(
                    existing_application,
                    operator_username=student["phone_number"],
                )
                if resubmitting_rejected_application and workflow_task is not None:
                    workflow_task["latest_comment"] = "学生重新提交申请，等待重新审核。"
                    workflow_task.setdefault("history", []).append(
                        {
                            "operated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "operator_username": student["phone_number"],
                            "operator_full_name": student["full_name"],
                            "action": "resubmit",
                            "action_label": "重新提交",
                            "from_node": "流程结束",
                            "to_node": workflow_task.get("current_node") or "资格审核",
                            "result_status": workflow_task.get("status") or "待处理",
                            "comment": workflow_task["latest_comment"],
                        }
                    )
                    task_changed = True
                if task_changed and workflow_task is not None:
                    workflow_located = self._workflow_task_index_by_business_key(str(existing_application.get("business_key") or ""))
                    if workflow_located is not None:
                        self._list("workflow_tasks")[workflow_located[0]] = workflow_task
                business_key = str(existing_application["business_key"])
                application_status = str(existing_application["application_status"])
                persisted_application = existing_application
            else:
                persisted_application = self._workflow_initial_item(
                    "recruitment_application",
                    RecruitApplicationUpsert(
                        plan_id=payload.plan_id,
                        student_name=student["full_name"],
                        gender=payload.gender,
                        graduation_school=graduation_school,
                        highest_degree=highest_degree,
                        intended_field=intended_field,
                        first_choice_team_id=selected_team_id,
                        first_choice=advisor_name,
                        second_choice_team_id=second_choice_team_id,
                        second_choice=second_choice,
                        political_status=payload.political_status,
                        marital_status=payload.marital_status,
                        religious_belief=payload.religious_belief,
                        native_place=payload.native_place,
                        mailing_address=payload.mailing_address,
                        id_type=payload.id_type,
                        phone_number=student["phone_number"],
                        email=student["email"],
                        id_number=student["id_number"],
                        intended_advisor_user_id=selected_advisor_user_id,
                        intended_advisor_name=advisor_name,
                        family_info=payload.family_info,
                        education_experience=payload.education_experience,
                        practice_experience=payload.practice_experience,
                        personal_statement_text=payload.personal_statement_text,
                        personal_statement_attachment=(payload.personal_statement.resume_attachment_url if payload.personal_statement else None),
                        supplementary_profile=payload.personal_profile,
                        self_evaluation=payload.self_evaluation,
                        discovery_channel=payload.source_channel_other or payload.source_channel,
                        source_channel=payload.source_channel,
                        source_channel_other=payload.source_channel_other,
                        portal_student_id=student_id,
                        applied_at=submitted_at,
                        material_status="待审核",
                        application_status="报名已提交",
                    ).model_dump(),
                )
                persisted_application["id"] = self._next_id("recruitment_applications")
                self._list("recruitment_applications").insert(0, persisted_application)
                self._start_managed_workflow("recruitment_application", persisted_application, operator_username=student["phone_number"])
                workflow_located = self._workflow_task_index_by_business_key(str(persisted_application.get("business_key") or ""))
                workflow_task = workflow_located[1] if workflow_located is not None else None
                created_application = True
                created_workflow_task = workflow_located is not None
                business_key = str(persisted_application["business_key"])
                application_status = str(persisted_application["application_status"])

            try:
                if persisted_application is not None:
                    self._persist_portal_application_submission(
                        student,
                        persisted_application,
                        None,
                        workflow_task=workflow_task,
                        created_application=created_application,
                        created_workflow_task=created_workflow_task,
                    )
                else:
                    self._persist_portal_student_change(student, None)
            except Exception:
                self._save()
            return PortalApplicationSubmissionResponse(
                student=self.get_portal_student(student_id),
                application_business_key=business_key,
                application_status=application_status,
            )
