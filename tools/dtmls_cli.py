from __future__ import annotations

import argparse
import configparser
import os
import getpass
import json
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, parse, request

import psycopg
from psycopg.rows import dict_row

if os.name == 'nt':
    import msvcrt


INI_FILE_NAME = 'dtmls_cli.ini'
DEFAULT_HOST = '47.117.107.23'
DEFAULT_PORT = 15431
DEFAULT_DATABASE = 'db_dtlms'
DEFAULT_USER = 'postgre'
DEFAULT_ALT_USER = 'postgres'
DEFAULT_SCHEMA = 'public'
DEFAULT_API_BASE_URL = 'http://127.0.0.1:8000/api/v1'
DEFAULT_SESSION_FILE = 'dtmls_cli.session.json'


def get_runtime_base_dir() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


@dataclass(slots=True)
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str
    schema: str
    connect_timeout: int
    alt_user: str | None = None

    @classmethod
    def from_parser(cls, parser: configparser.ConfigParser) -> 'DatabaseConfig':
        if 'postgres' not in parser:
            raise ValueError('配置文件缺少 [postgres] 段')

        section = parser['postgres']
        password = section.get('password', '').strip()
        if not password:
            raise ValueError('INI 配置中的 postgres.password 不能为空')

        return cls(
            host=section.get('host', DEFAULT_HOST).strip(),
            port=section.getint('port', DEFAULT_PORT),
            database=section.get('database', DEFAULT_DATABASE).strip(),
            user=section.get('user', DEFAULT_USER).strip(),
            password=password,
            schema=section.get('schema', DEFAULT_SCHEMA).strip(),
            connect_timeout=section.getint('connect_timeout', 8),
            alt_user=section.get('alt_user', DEFAULT_ALT_USER).strip() or None,
        )

    def candidate_users(self) -> list[str]:
        users = [self.user]
        if self.alt_user:
            users.append(self.alt_user)
        deduped: list[str] = []
        for item in users:
            if item not in deduped:
                deduped.append(item)
        return deduped

    def dsn(self, username: str) -> str:
        return (
            f'host={self.host} '
            f'port={self.port} '
            f'dbname={self.database} '
            f'user={username} '
            f'password={self.password} '
            f'connect_timeout={self.connect_timeout} '
            'client_encoding=utf8'
        )


@dataclass(slots=True)
class ApiConfig:
    base_url: str
    verify_tls: bool
    session_file: str

    @classmethod
    def from_parser(cls, parser: configparser.ConfigParser) -> 'ApiConfig':
        section = parser['api'] if 'api' in parser else {}
        verify_text = str(section.get('verify_tls', 'true')).strip().lower()
        return cls(
            base_url=str(section.get('base_url', DEFAULT_API_BASE_URL)).strip().rstrip('/'),
            verify_tls=verify_text not in {'0', 'false', 'no'},
            session_file=str(section.get('session_file', DEFAULT_SESSION_FILE)).strip() or DEFAULT_SESSION_FILE,
        )


@dataclass(slots=True)
class AppConfig:
    database: DatabaseConfig
    api: ApiConfig
    ini_path: Path
    base_dir: Path

    @classmethod
    def load(cls, ini_path: Path) -> 'AppConfig':
        parser = configparser.ConfigParser()
        if not ini_path.exists():
            raise FileNotFoundError(f'未找到配置文件: {ini_path}')
        parser.read(ini_path, encoding='utf-8-sig')
        return cls(
            database=DatabaseConfig.from_parser(parser),
            api=ApiConfig.from_parser(parser),
            ini_path=ini_path,
            base_dir=ini_path.parent,
        )


class SessionStore:
    def __init__(self, session_path: Path) -> None:
        self.session_path = session_path
        self.data: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        if not self.session_path.exists():
            self.data = {}
            return
        try:
            self.data = json.loads(self.session_path.read_text(encoding='utf-8'))
        except Exception:
            self.data = {}

    def save(self) -> None:
        self.session_path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding='utf-8')

    def clear(self) -> None:
        self.data = {}
        if self.session_path.exists():
            self.session_path.unlink()

    @property
    def access_token(self) -> str | None:
        return self.data.get('access_token')

    @property
    def refresh_token(self) -> str | None:
        return self.data.get('refresh_token')

    @property
    def principal(self) -> dict[str, Any] | None:
        value = self.data.get('principal')
        return value if isinstance(value, dict) else None

    @property
    def profile(self) -> dict[str, Any] | None:
        value = self.data.get('profile')
        return value if isinstance(value, dict) else None

    def update(self, payload: dict[str, Any]) -> None:
        self.data.update(payload)
        self.save()


class ApiError(RuntimeError):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code


class ApiClient:
    def __init__(self, config: ApiConfig, session: SessionStore) -> None:
        self.config = config
        self.session = session

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | list[Any] | None = None,
        form_body: dict[str, Any] | None = None,
        require_auth: bool = True,
    ) -> Any:
        url = f'{self.config.base_url}{path}'
        if params:
            clean_params = {key: value for key, value in params.items() if value is not None and value != ''}
            if clean_params:
                url = f'{url}?{parse.urlencode(clean_params)}'

        headers = {'Accept': 'application/json'}
        data: bytes | None = None
        if require_auth:
            if not self.session.access_token:
                raise RuntimeError('当前未登录，请先执行 /login')
            headers['Authorization'] = f'Bearer {self.session.access_token}'

        if json_body is not None:
            headers['Content-Type'] = 'application/json; charset=utf-8'
            data = json.dumps(json_body, ensure_ascii=False).encode('utf-8')
        elif form_body is not None:
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=utf-8'
            data = parse.urlencode(form_body).encode('utf-8')

        req = request.Request(url, method=method.upper(), headers=headers, data=data)
        try:
            with request.urlopen(req) as response:
                if response.status == 204:
                    return None
                body = response.read().decode('utf-8')
                return json.loads(body) if body else None
        except error.HTTPError as exc:
            body = exc.read().decode('utf-8', errors='ignore')
            message = body
            try:
                payload = json.loads(body)
                message = payload.get('detail') or payload.get('message') or body
            except Exception:
                pass
            if exc.code == 401:
                self.session.clear()
            raise ApiError(exc.code, f'API {exc.code}: {message}') from exc
        except error.URLError as exc:
            raise RuntimeError(f'无法连接后端接口 {self.config.base_url}，请确认后端已启动。') from exc

    def login(self, username: str, password: str) -> dict[str, Any]:
        return self.request(
            'POST',
            '/auth/token',
            form_body={'username': username, 'password': password, 'grant_type': 'password'},
            require_auth=False,
        )

    def get_me(self) -> dict[str, Any]:
        return self.request('GET', '/auth/me')

    def get_profile(self) -> dict[str, Any]:
        return self.request('GET', '/auth/profile')

    def update_profile(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.request('PUT', '/auth/profile', json_body=payload)

    def change_password(self, current_password: str, new_password: str) -> dict[str, Any]:
        return self.request(
            'POST',
            '/auth/change-password',
            json_body={'current_password': current_password, 'new_password': new_password},
        )

    def list_students(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request('GET', '/students/management', params=params)

    def student_stats(self) -> dict[str, Any]:
        return self.request('GET', '/students/management/stats')

    def delete_student(self, student_id: int) -> None:
        self.request('DELETE', f'/students/management/{student_id}')

    def recruitment_stats(self) -> dict[str, Any]:
        return self.request('GET', '/recruitment/stats')

    def recruitment_plans(self) -> dict[str, Any]:
        return self.request('GET', '/recruitment/plans')

    def recruitment_applications(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request('GET', '/recruitment/applications', params=params)

    def training_stats(self) -> dict[str, Any]:
        return self.request('GET', '/training/stats')

    def training_plans(self) -> dict[str, Any]:
        return self.request('GET', '/training/plans')

    def training_reports(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request('GET', '/training/reports', params=params)

    def training_outbound(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request('GET', '/training/outbound-studies', params=params)

    def degree_stats(self) -> dict[str, Any]:
        return self.request('GET', '/degree/stats')

    def degree_theses(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request('GET', '/degree/theses', params=params)

    def degree_reviews(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request('GET', '/degree/reviews', params=params)

    def workflow_stats(self) -> dict[str, Any]:
        return self.request('GET', '/workflow/stats')

    def workflow_tasks(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.request('GET', '/workflow/tasks', params=params)

    def system_stats(self) -> dict[str, Any]:
        return self.request('GET', '/system/stats')

    def system_users(self) -> dict[str, Any]:
        return self.request('GET', '/system/users')

    def system_roles(self) -> dict[str, Any]:
        return self.request('GET', '/system/roles')

    def audit_policies(self) -> dict[str, Any]:
        return self.request('GET', '/system/audit-policies')

    def integrations(self) -> dict[str, Any]:
        return self.request('GET', '/system/integrations')

    def operation_logs(self) -> dict[str, Any]:
        return self.request('GET', '/system/operation-logs')

    def sync_logs(self) -> dict[str, Any]:
        return self.request('GET', '/system/sync-logs')

    def architecture(self) -> dict[str, Any]:
        return self.request('GET', '/system/architecture')


class StudentDeleteCli:
    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config

    def connect(self) -> psycopg.Connection[Any]:
        last_error: Exception | None = None
        for username in self.config.candidate_users():
            try:
                connection = psycopg.connect(self.config.dsn(username), row_factory=dict_row)
                with connection.cursor() as cursor:
                    cursor.execute(f'SET search_path TO {self.config.schema}, public')
                return connection
            except Exception as exc:
                last_error = exc
        if last_error is None:
            raise RuntimeError('没有可用的数据库连接账号')
        raise last_error

    def find_student(self, cursor: psycopg.Cursor[Any], student_no: str) -> dict[str, Any] | None:
        cursor.execute(
            '''
            SELECT
                s.id,
                s.student_no,
                s.full_name,
                s.degree_type,
                s.enrollment_year,
                s.team_name,
                s.current_status,
                s.phone_number,
                s.political_status,
                COALESCE(a.full_name, '') AS advisor_name
            FROM dtlms_students AS s
            LEFT JOIN dtlms_advisors AS a ON a.id = s.primary_advisor_id
            WHERE s.student_no = %s AND s.is_deleted = FALSE
            ''',
            (student_no,),
        )
        row = cursor.fetchone()
        if row is not None:
            return dict(row)

        cursor.execute(
            '''
            SELECT
                id,
                payload->>'student_no' AS student_no,
                payload->>'full_name' AS full_name,
                payload->>'degree_type' AS degree_type,
                NULLIF(payload->>'enrollment_year', '')::INTEGER AS enrollment_year,
                payload->>'team_name' AS team_name,
                payload->>'status' AS current_status,
                payload->>'phone_number' AS phone_number,
                payload->>'political_status' AS political_status,
                payload->>'advisor_name' AS advisor_name
            FROM dtlms_runtime_students
            WHERE payload->>'student_no' = %s
            ''',
            (student_no,),
        )
        row = cursor.fetchone()
        return dict(row) if row is not None else None

    def collect_related_counts(self, cursor: psycopg.Cursor[Any], student_id: int, student_no: str) -> dict[str, int]:
        counts: dict[str, int] = {}
        queries = {
            '导师关系': ('SELECT COUNT(*) AS total FROM dtlms_student_advisor_history WHERE student_id = %s', (student_id,)),
            '培养方案': ('SELECT COUNT(*) AS total FROM dtlms_training_plans WHERE student_id = %s AND is_deleted = FALSE', (student_id,)),
            '科研报告': ('SELECT COUNT(*) AS total FROM dtlms_scientific_reports WHERE student_id = %s AND is_deleted = FALSE', (student_id,)),
            '外出研修': ('SELECT COUNT(*) AS total FROM dtlms_outbound_studies WHERE student_id = %s AND is_deleted = FALSE', (student_id,)),
            '论文主档': ('SELECT COUNT(*) AS total FROM dtlms_theses WHERE student_id = %s AND is_deleted = FALSE', (student_id,)),
            '运行时学生': ("SELECT COUNT(*) AS total FROM dtlms_runtime_students WHERE payload->>'student_no' = %s", (student_no,)),
            '运行时培养方案': ("SELECT COUNT(*) AS total FROM dtlms_runtime_training_plans WHERE payload->>'student_no' = %s", (student_no,)),
            '运行时科研报告': ("SELECT COUNT(*) AS total FROM dtlms_runtime_scientific_reports WHERE payload->>'student_no' = %s", (student_no,)),
            '运行时外出研修': ("SELECT COUNT(*) AS total FROM dtlms_runtime_outbound_studies WHERE payload->>'student_no' = %s", (student_no,)),
            '运行时论文': ("SELECT COUNT(*) AS total FROM dtlms_runtime_theses WHERE payload->>'student_no' = %s", (student_no,)),
        }
        for label, (query, params) in queries.items():
            cursor.execute(query, params)
            counts[label] = int(cursor.fetchone()['total'])

        cursor.execute(
            '''
            SELECT COUNT(*) AS total
            FROM dtlms_thesis_reviews
            WHERE thesis_id IN (SELECT id FROM dtlms_theses WHERE student_id = %s)
            ''',
            (student_id,),
        )
        counts['论文评阅'] = int(cursor.fetchone()['total'])

        cursor.execute(
            '''
            SELECT COUNT(*) AS total
            FROM dtlms_runtime_thesis_reviews
            WHERE NULLIF(payload->>'thesis_id', '')::BIGINT IN (
                SELECT id FROM dtlms_theses WHERE student_id = %s
            )
            ''',
            (student_id,),
        )
        counts['运行时论文评阅'] = int(cursor.fetchone()['total'])
        return counts

    def lookup_student(self, student_no: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            with connection.cursor() as cursor:
                return self.find_student(cursor, student_no.strip())

    def delete_student(self, student_no: str, confirm: bool = True) -> int:
        normalized_student_no = student_no.strip()
        if not normalized_student_no:
            print('学号不能为空。')
            return 2

        with self.connect() as connection:
            with connection.cursor() as cursor:
                student = self.find_student(cursor, normalized_student_no)
                if student is None:
                    print(f'未找到学号为 {normalized_student_no} 的学生。')
                    return 1

                self.print_student_info(cursor, student)

                if confirm and not self.confirm_delete():
                    print('已取消删除。')
                    connection.rollback()
                    return 0

                self.perform_delete(cursor, student)
                connection.commit()

        print(f'已删除学生 {student["full_name"]}（{student["student_no"]}）。')
        return 0

    def print_student_info(self, cursor: psycopg.Cursor[Any], student: dict[str, Any]) -> None:
        counts = self.collect_related_counts(cursor, int(student['id']), str(student['student_no']))
        print('找到学生信息：')
        print(f'  学号: {student["student_no"]}')
        print(f'  姓名: {student["full_name"]}')
        print(f'  学位类型: {student.get("degree_type") or "-"}')
        print(f'  导师: {student.get("advisor_name") or "-"}')
        print(f'  团队: {student.get("team_name") or "-"}')
        print(f'  入学年份: {student.get("enrollment_year") or "-"}')
        print(f'  当前状态: {student.get("current_status") or "-"}')
        print('  关联记录:')
        for label, total in counts.items():
            print(f'    - {label}: {total}')

    @staticmethod
    def confirm_delete() -> bool:
        while True:
            answer = input('确认删除该学生及其关联记录吗？请输入 Y/N: ').strip().lower()
            if answer in {'y', 'yes'}:
                return True
            if answer in {'n', 'no'}:
                return False
            print('输入无效，请输入 Y 或 N。')

    def perform_delete(self, cursor: psycopg.Cursor[Any], student: dict[str, Any]) -> None:
        student_id = int(student['id'])
        student_no = str(student['student_no'])

        cursor.execute('SELECT id FROM dtlms_training_plans WHERE student_id = %s', (student_id,))
        training_plan_ids = [int(row['id']) for row in cursor.fetchall()]

        cursor.execute('SELECT id FROM dtlms_theses WHERE student_id = %s', (student_id,))
        thesis_ids = [int(row['id']) for row in cursor.fetchall()]

        if thesis_ids:
            cursor.execute('DELETE FROM dtlms_thesis_reviews WHERE thesis_id = ANY(%s)', (thesis_ids,))
            cursor.execute(
                "DELETE FROM dtlms_runtime_thesis_reviews WHERE NULLIF(payload->>'thesis_id', '')::BIGINT = ANY(%s)",
                (thesis_ids,),
            )

        if training_plan_ids:
            cursor.execute('DELETE FROM dtlms_training_plan_versions WHERE training_plan_id = ANY(%s)', (training_plan_ids,))

        cursor.execute('DELETE FROM dtlms_scientific_reports WHERE student_id = %s', (student_id,))
        cursor.execute('DELETE FROM dtlms_outbound_studies WHERE student_id = %s', (student_id,))
        cursor.execute('DELETE FROM dtlms_achievements WHERE student_id = %s', (student_id,))
        cursor.execute('DELETE FROM dtlms_training_plans WHERE student_id = %s', (student_id,))
        cursor.execute('DELETE FROM dtlms_student_advisor_history WHERE student_id = %s', (student_id,))
        cursor.execute('DELETE FROM dtlms_theses WHERE student_id = %s', (student_id,))
        cursor.execute('DELETE FROM dtlms_students WHERE id = %s', (student_id,))

        cursor.execute("DELETE FROM dtlms_runtime_scientific_reports WHERE payload->>'student_no' = %s", (student_no,))
        cursor.execute("DELETE FROM dtlms_runtime_outbound_studies WHERE payload->>'student_no' = %s", (student_no,))
        cursor.execute("DELETE FROM dtlms_runtime_training_plans WHERE payload->>'student_no' = %s", (student_no,))
        cursor.execute("DELETE FROM dtlms_runtime_theses WHERE payload->>'student_no' = %s", (student_no,))
        cursor.execute("DELETE FROM dtlms_runtime_students WHERE payload->>'student_no' = %s", (student_no,))

        cursor.execute(
            '''
            INSERT INTO dtlms_operation_logs (
                operator_username,
                operator_role,
                module_name,
                entity_name,
                entity_id,
                action,
                old_value,
                new_value,
                request_ip,
                result
            ) VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, %s, %s)
            ''',
            (
                'dtmls_cli',
                'cli',
                '学生管理',
                '学生主档',
                str(student_id),
                '删除',
                self.to_json(
                    {
                        'student_no': student_no,
                        'full_name': student['full_name'],
                        'advisor_name': student.get('advisor_name'),
                    }
                ),
                self.to_json({'source': 'dtmls_cli'}),
                '127.0.0.1',
                'success',
            ),
        )

    @staticmethod
    def to_json(payload: dict[str, Any]) -> str:
        return json.dumps(payload, ensure_ascii=False)


class DtmlsShell:
    QUICK_MENU_ACTIONS: list[tuple[str, str]] = [
        ('登录系统', 'login'),
        ('查看当前身份', 'whoami'),
        ('查看学生统计', 'students stats'),
        ('查看学生列表', 'students list'),
        ('查看招生计划', 'recruitment plans'),
        ('查看待办任务', 'workflow tasks status=待处理'),
        ('查看系统用户', 'system users'),
        ('查看当前配置', 'config'),
        ('显示完整帮助', 'help'),
        ('退出 CLI', 'exit'),
    ]

    def __init__(self, app_config: AppConfig) -> None:
        self.app_config = app_config
        self.session = SessionStore(app_config.base_dir / app_config.api.session_file)
        self.api = ApiClient(app_config.api, self.session)
        self.db_cli = StudentDeleteCli(app_config.database)

    def run_repl(self) -> int:
        self.print_banner()
        while True:
            try:
                raw = self.read_repl_command()
            except EOFError:
                print()
                return 0
            except KeyboardInterrupt:
                print('\n操作已中断。')
                return 130

            if raw is None or not raw:
                continue
            code = self.execute(raw)
            if code == 999:
                return 0

    def execute(self, raw: str) -> int:
        parts = shlex.split(raw)
        if not parts:
            return 0
        return self.execute_parts(parts)

    def execute_parts(self, parts: list[str]) -> int:
        raw_command = parts[0].lower()
        if raw_command == '/':
            return self.open_quick_menu_text()
        command = raw_command.lstrip('/')
        args = parts[1:]

        try:
            if command in {'help', 'commands'}:
                self.print_help()
                return 0
            if command in {'exit', 'quit'}:
                return 999
            if command == 'config':
                self.show_config()
                return 0
            if command == 'login':
                return self.command_login(args)
            if command == 'logout':
                self.session.clear()
                print('已退出登录并清除本地会话。')
                return 0
            if command == 'whoami':
                return self.command_whoami()
            if command == 'profile':
                return self.command_profile(args)
            if command == 'passwd':
                return self.command_passwd()
            if command == 'students':
                return self.command_students(args)
            if command == 'student':
                return self.command_student(args)
            if command == 'recruitment':
                return self.command_recruitment(args)
            if command == 'training':
                return self.command_training(args)
            if command == 'degree':
                return self.command_degree(args)
            if command == 'workflow':
                return self.command_workflow(args)
            if command == 'system':
                return self.command_system(args)
            if command == 'api':
                return self.command_api(args)
            if command == 'delete' and len(args) == 1:
                return self.db_cli.delete_student(args[0])
            if command == 'show' and len(args) == 1:
                return self.show_student(args[0])
            print('无法识别命令。输入 help 查看可用命令。')
            return 2
        except ApiError as exc:
            print(str(exc))
            return 1
        except Exception as exc:
            print(f'执行失败: {exc}')
            return 1

    def print_banner(self) -> None:
        print('DTLMS CLI 已启动。直接输入命令即可，按 / 可立即打开快捷菜单，输入 help 查看完整命令。')
        print('常用直达命令: delete 学号, show 学号, students stats, system users')

    @staticmethod
    def supports_keypress_menu() -> bool:
        return os.name == 'nt' and sys.stdin.isatty() and sys.stdout.isatty()

    def read_repl_command(self) -> str | None:
        if not self.supports_keypress_menu():
            raw = input('dtmls> ').strip()
            if raw == '/':
                code = self.open_quick_menu_text()
                if code == 999:
                    return 'exit'
                return None
            return raw or None

        print('dtmls> ', end='', flush=True)
        buffer: list[str] = []
        while True:
            key = msvcrt.getwch()
            if key in {'\r', '\n'}:
                print()
                raw = ''.join(buffer).strip()
                return raw or None
            if key == '\x03':
                raise KeyboardInterrupt
            if key in {'\x08', '\x7f'}:
                if buffer:
                    buffer.pop()
                    print('\b \b', end='', flush=True)
                continue
            if key in {'\x00', '\xe0'}:
                _ = msvcrt.getwch()
                continue
            if key == '/' and not buffer:
                print()
                code = self.open_quick_menu_arrow()
                if code == 999:
                    return 'exit'
                return None
            if key.isprintable():
                buffer.append(key)
                print(key, end='', flush=True)

    def open_quick_menu_text(self) -> int:
        print('快捷菜单：')
        for index, (label, action) in enumerate(self.QUICK_MENU_ACTIONS, start=1):
            print(f'  {index}. {label} -> {action}')
        print('  0. 返回命令输入')

        choice = input('请选择序号并回车，直接回车返回: ').strip()
        if not choice or choice == '0':
            return 0

        if not choice.isdigit():
            print('无效序号，请重新输入 / 打开菜单。')
            return 2

        index = int(choice) - 1
        if 0 <= index < len(self.QUICK_MENU_ACTIONS):
            return self.execute(self.QUICK_MENU_ACTIONS[index][1])

        print('无效序号，请重新输入 / 打开菜单。')
        return 2

    def open_quick_menu_arrow(self) -> int:
        selected = 0
        self.render_quick_menu(selected)
        while True:
            key = msvcrt.getwch()
            if key in {'\x00', '\xe0'}:
                arrow = msvcrt.getwch()
                if arrow == 'H':
                    selected = (selected - 1) % len(self.QUICK_MENU_ACTIONS)
                    self.render_quick_menu(selected)
                    continue
                if arrow == 'P':
                    selected = (selected + 1) % len(self.QUICK_MENU_ACTIONS)
                    self.render_quick_menu(selected)
                    continue
                continue
            if key in {'\r', '\n'}:
                print()
                return self.execute(self.QUICK_MENU_ACTIONS[selected][1])
            if key == '\x1b':
                print()
                return 0
            if key == '/':
                print()
                return 0

    def render_quick_menu(self, selected: int) -> None:
        sys.stdout.write('\x1b[2J\x1b[H')
        print('快捷菜单（↑↓选择，Enter 执行，Esc 返回）')
        print('')
        for index, (label, action) in enumerate(self.QUICK_MENU_ACTIONS):
            prefix = '>' if index == selected else ' '
            print(f'{prefix} {label:<12} {action}')
        print('')
        print('按 Esc 返回命令输入。')
        sys.stdout.flush()

    def print_help(self) -> None:
        print('可用命令：')
        print('  help 或 /help                      显示帮助')
        print('  login [用户名]                     登录后端接口，密码会安全输入')
        print('  logout                             清除本地会话')
        print('  whoami                             查看当前登录身份')
        print('  profile                            查看个人资料')
        print('  profile set key=value ...          更新个人资料，可改 full_name/phone_number/email/theme_color')
        print('  passwd                             交互修改当前登录用户密码')
        print('  students stats                     查看学生统计')
        print('  students list [keyword=] [status=] [advisor=]')
        print('  student show 学号                  查看指定学生')
        print('  student delete 学号                优先走 API 删除，未登录时走数据库直删')
        print('  recruitment stats|plans|applications [keyword=] [status=] [plan_id=]')
        print('  training stats|plans|reports|outbound [keyword=] [status=]')
        print('  degree stats|theses|reviews [keyword=] [status=] [thesis_id=]')
        print('  workflow stats|tasks [status=] [module=]')
        print('  system stats|users|roles|audit-policies|integrations|operation-logs|sync-logs|architecture')
        print('  api METHOD PATH [key=value ...]       通用接口调用，覆盖未单独封装的 Web 操作')
        print('  config                             查看当前 INI 与会话文件位置')
        print('  exit                               退出 CLI')
        print('')
        print('直达命令：')
        print('  delete 学号                        直连数据库确认删除')
        print('  show 学号                          查看指定学生')

    def show_config(self) -> None:
        print(f'INI 文件: {self.app_config.ini_path}')
        print(f'会话文件: {self.app_config.base_dir / self.app_config.api.session_file}')
        print(f'API 地址: {self.app_config.api.base_url}')
        print(f'DB 地址: {self.app_config.database.host}:{self.app_config.database.port}/{self.app_config.database.database}')

    def command_login(self, args: list[str]) -> int:
        username = args[0] if args else input('用户名: ').strip()
        if not username:
            print('用户名不能为空。')
            return 2
        password = getpass.getpass('密码: ')
        token = self.api.login(username, password)
        self.session.update({'access_token': token['access_token'], 'refresh_token': token['refresh_token']})
        principal = self.api.get_me()
        profile = self.api.get_profile()
        self.session.update({'principal': principal, 'profile': profile})
        print(f'登录成功：{principal["full_name"]}（{principal["username"]}）')
        return 0

    def command_whoami(self) -> int:
        if not self.session.access_token:
            print('当前未登录。')
            return 1
        principal = self.api.get_me()
        profile = self.api.get_profile()
        self.session.update({'principal': principal, 'profile': profile})
        print(f'用户名: {principal["username"]}')
        print(f'姓名: {principal["full_name"]}')
        print(f'角色: {" / ".join(principal.get("roles", [])) or "-"}')
        print(f'部门: {profile.get("department_name") or "-"}')
        return 0

    def command_profile(self, args: list[str]) -> int:
        if not args:
            profile = self.api.get_profile()
            self.session.update({'profile': profile})
            self.print_kv(profile)
            return 0
        if args[0].lower() != 'set':
            print('用法: /profile 或 /profile set key=value ...')
            return 2
        updates = self.parse_key_value_args(args[1:])
        if not updates:
            print('至少需要提供一个 key=value 参数。')
            return 2
        current = self.api.get_profile()
        payload = {
            'full_name': updates.get('full_name', current['full_name']),
            'phone_number': updates.get('phone_number', current.get('phone_number') or ''),
            'email': updates.get('email', current.get('email') or ''),
            'theme_color': updates.get('theme_color', current['theme_color']),
        }
        profile = self.api.update_profile(payload)
        self.session.update({'profile': profile})
        print('个人资料已更新。')
        self.print_kv(profile)
        return 0

    def command_passwd(self) -> int:
        current_password = getpass.getpass('当前密码: ')
        new_password = getpass.getpass('新密码: ')
        confirm_password = getpass.getpass('确认新密码: ')
        if not current_password or not new_password:
            print('密码不能为空。')
            return 2
        if new_password != confirm_password:
            print('两次输入的新密码不一致。')
            return 2
        self.api.change_password(current_password, new_password)
        print('密码已更新。')
        return 0

    def command_students(self, args: list[str]) -> int:
        if not args:
            print('用法: /students stats 或 /students list [keyword=] [status=] [advisor=]')
            return 2
        action = args[0].lower()
        if action == 'stats':
            self.print_kv(self.api.student_stats())
            return 0
        if action == 'list':
            filters = self.parse_key_value_args(args[1:])
            params = {
                'keyword': filters.get('keyword'),
                'status': filters.get('status'),
                'advisor_name': filters.get('advisor') or filters.get('advisor_name'),
            }
            payload = self.api.list_students(params)
            self.print_table(
                payload.get('items', []),
                ['student_no', 'full_name', 'status', 'advisor_name', 'team_name', 'degree_type', 'enrollment_year'],
            )
            print(f'总数: {payload.get("total", 0)}')
            return 0
        print('仅支持 /students stats 或 /students list')
        return 2

    def command_student(self, args: list[str]) -> int:
        if len(args) < 2:
            print('用法: /student show 学号 或 /student delete 学号')
            return 2
        action = args[0].lower()
        student_no = args[1].strip()
        if action == 'show':
            return self.show_student(student_no)
        if action == 'delete':
            if self.session.access_token:
                return self.delete_student_via_api(student_no)
            return self.db_cli.delete_student(student_no)
        print('仅支持 /student show 或 /student delete')
        return 2

    def command_recruitment(self, args: list[str]) -> int:
        if not args:
            print('用法: /recruitment stats|plans|applications')
            return 2
        action = args[0].lower()
        if action == 'stats':
            self.print_kv(self.api.recruitment_stats())
            return 0
        if action == 'plans':
            payload = self.api.recruitment_plans()
            self.print_table(payload.get('items', []), ['id', 'plan_name', 'academic_term', 'current_stage', 'target_quota', 'application_count', 'is_open'])
            return 0
        if action == 'applications':
            filters = self.parse_key_value_args(args[1:])
            payload = self.api.recruitment_applications(filters)
            self.print_table(payload.get('items', []), ['id', 'candidate_no', 'student_name', 'graduation_school', 'intended_field', 'material_status', 'application_status'])
            print(f'总数: {payload.get("total", 0)}')
            return 0
        print('仅支持 /recruitment stats|plans|applications')
        return 2

    def command_training(self, args: list[str]) -> int:
        if not args:
            print('用法: /training stats|plans|reports|outbound')
            return 2
        action = args[0].lower()
        if action == 'stats':
            self.print_kv(self.api.training_stats())
            return 0
        filters = self.parse_key_value_args(args[1:])
        if action == 'plans':
            payload = self.api.training_plans()
            self.print_table(payload.get('items', []), ['id', 'student_no', 'student_name', 'advisor_name', 'version_no', 'report_cycle', 'plan_status'])
            return 0
        if action == 'reports':
            payload = self.api.training_reports({'keyword': filters.get('keyword'), 'status': filters.get('status')})
            self.print_table(payload.get('items', []), ['id', 'student_no', 'student_name', 'period_label', 'report_status', 'reviewer_name', 'review_score'])
            return 0
        if action == 'outbound':
            payload = self.api.training_outbound({'keyword': filters.get('keyword'), 'status': filters.get('status')})
            self.print_table(payload.get('items', []), ['id', 'student_no', 'student_name', 'study_type', 'destination', 'approval_status'])
            return 0
        print('仅支持 /training stats|plans|reports|outbound')
        return 2

    def command_degree(self, args: list[str]) -> int:
        if not args:
            print('用法: /degree stats|theses|reviews')
            return 2
        action = args[0].lower()
        if action == 'stats':
            self.print_kv(self.api.degree_stats())
            return 0
        filters = self.parse_key_value_args(args[1:])
        if action == 'theses':
            payload = self.api.degree_theses({'keyword': filters.get('keyword'), 'degree_status': filters.get('status') or filters.get('degree_status')})
            self.print_table(payload.get('items', []), ['id', 'student_no', 'student_name', 'title', 'thesis_status', 'blind_review_status', 'degree_status'])
            return 0
        if action == 'reviews':
            payload = self.api.degree_reviews({'thesis_id': filters.get('thesis_id')})
            self.print_table(payload.get('items', []), ['id', 'thesis_id', 'thesis_title', 'expert_name', 'review_score', 'review_status'])
            return 0
        print('仅支持 /degree stats|theses|reviews')
        return 2

    def command_workflow(self, args: list[str]) -> int:
        if not args:
            print('用法: /workflow stats|tasks')
            return 2
        action = args[0].lower()
        if action == 'stats':
            self.print_kv(self.api.workflow_stats())
            return 0
        if action == 'tasks':
            filters = self.parse_key_value_args(args[1:])
            payload = self.api.workflow_tasks({'status': filters.get('status'), 'module': filters.get('module')})
            self.print_table(payload.get('items', []), ['id', 'workflow_name', 'business_key', 'title', 'status', 'current_handler', 'applicant_name'])
            return 0
        print('仅支持 /workflow stats|tasks')
        return 2

    def command_system(self, args: list[str]) -> int:
        if not args:
            print('用法: /system stats|users|roles|audit-policies|integrations|operation-logs|sync-logs|architecture')
            return 2
        action = args[0].lower()
        if action == 'stats':
            self.print_kv(self.api.system_stats())
            return 0
        if action == 'users':
            payload = self.api.system_users()
            self.print_table(payload.get('items', []), ['id', 'username', 'full_name', 'role_name', 'department_name', 'account_status'])
            return 0
        if action == 'roles':
            payload = self.api.system_roles()
            self.print_table(payload.get('items', []), ['id', 'role_code', 'role_name', 'scope_name'])
            return 0
        if action == 'audit-policies':
            payload = self.api.audit_policies()
            self.print_table(payload.get('items', []), ['id', 'item', 'policy'])
            return 0
        if action == 'integrations':
            payload = self.api.integrations()
            self.print_table(payload.get('items', []), ['id', 'name', 'direction', 'cadence', 'status', 'owner'])
            return 0
        if action == 'operation-logs':
            payload = self.api.operation_logs()
            self.print_table(payload.get('items', []), ['id', 'operated_at', 'operator_username', 'module_name', 'action', 'result'])
            return 0
        if action == 'sync-logs':
            payload = self.api.sync_logs()
            self.print_table(payload.get('items', []), ['id', 'executed_at', 'source_system', 'target_system', 'sync_status', 'record_count'])
            return 0
        if action == 'architecture':
            payload = self.api.architecture()
            self.print_json(payload)
            return 0
        print('仅支持 /system stats|users|roles|audit-policies|integrations|operation-logs|sync-logs|architecture')
        return 2

    def command_api(self, args: list[str]) -> int:
        if len(args) < 2:
            print('用法: /api METHOD PATH [key=value ...]')
            print('示例: /api GET /system/users')
            print('示例: /api POST /students/management student_no=D20260001 full_name=张三 status=在校 advisor_name=刘亚 team_name=智能制造团队 degree_type=工程博士 enrollment_year=2026')
            return 2
        method = args[0].upper()
        path = args[1]
        if not path.startswith('/'):
            print('PATH 必须以 / 开头，例如 /students/management')
            return 2

        values = self.parse_key_value_args(args[2:])
        if method in {'GET', 'DELETE'}:
            payload = self.api.request(method, path, params=values)
        elif method in {'POST', 'PUT', 'PATCH'}:
            payload = self.api.request(method, path, json_body=self.normalize_scalar_values(values))
        else:
            print('METHOD 仅支持 GET/POST/PUT/PATCH/DELETE')
            return 2

        if payload is None:
            print('执行成功，无返回内容。')
            return 0
        if isinstance(payload, dict) and 'items' in payload:
            items = payload.get('items') or []
            if isinstance(items, list) and items:
                columns = list(items[0].keys())[:8]
                self.print_table(items, columns)
                if 'total' in payload:
                    print(f'总数: {payload.get("total")}')
                return 0
        self.print_json(payload)
        return 0

    def show_student(self, student_no: str) -> int:
        student = self.db_cli.lookup_student(student_no)
        if student is None:
            print(f'未找到学号为 {student_no} 的学生。')
            return 1
        print('学生信息：')
        self.print_kv(student)
        return 0

    def delete_student_via_api(self, student_no: str) -> int:
        payload = self.api.list_students({'keyword': student_no})
        match = next((item for item in payload.get('items', []) if item.get('student_no') == student_no), None)
        if match is None:
            print(f'未通过 API 找到学号为 {student_no} 的学生，回退数据库直删。')
            return self.db_cli.delete_student(student_no)
        self.print_kv(match)
        if not self.db_cli.confirm_delete():
            print('已取消删除。')
            return 0
        self.api.delete_student(int(match['id']))
        print(f'已通过 API 删除学生 {match["full_name"]}（{match["student_no"]}）。')
        return 0

    @staticmethod
    def parse_key_value_args(items: list[str]) -> dict[str, str]:
        values: dict[str, str] = {}
        for item in items:
            if '=' not in item:
                continue
            key, value = item.split('=', 1)
            values[key.strip()] = value.strip()
        return values

    @staticmethod
    def normalize_scalar_values(values: dict[str, str]) -> dict[str, Any]:
        normalized: dict[str, Any] = {}
        for key, value in values.items():
            lowered = value.lower()
            if lowered == 'true':
                normalized[key] = True
                continue
            if lowered == 'false':
                normalized[key] = False
                continue
            if lowered == 'null':
                normalized[key] = None
                continue
            if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                normalized[key] = int(value)
                continue
            try:
                if '.' in value:
                    normalized[key] = float(value)
                    continue
            except ValueError:
                pass
            normalized[key] = value
        return normalized

    @staticmethod
    def print_json(payload: Any) -> None:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    @staticmethod
    def print_kv(payload: dict[str, Any]) -> None:
        for key, value in payload.items():
            print(f'{key}: {value}')

    @staticmethod
    def print_table(items: list[dict[str, Any]], columns: list[str]) -> None:
        if not items:
            print('没有数据。')
            return
        rows = [[str(item.get(column, '')) for column in columns] for item in items]
        widths = [len(column) for column in columns]
        for row in rows:
            for index, cell in enumerate(row):
                widths[index] = min(max(widths[index], len(cell)), 32)
        header = ' | '.join(column.ljust(widths[index]) for index, column in enumerate(columns))
        separator = '-+-'.join('-' * width for width in widths)
        print(header)
        print(separator)
        for row in rows:
            normalized = [cell if len(cell) <= widths[index] else f'{cell[: widths[index] - 1]}…' for index, cell in enumerate(row)]
            print(' | '.join(normalized[index].ljust(widths[index]) for index in range(len(columns))))


def parse_inline_legacy_command(text: str) -> tuple[str, str] | None:
    value = text.strip()
    if not value:
        return None
    parts = shlex.split(value)
    if len(parts) == 2 and parts[0].lower() in {'delete', 'show'}:
        return (parts[0].lower(), parts[1].strip())
    return None


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='dtmls_cli',
        description='DTLMS 命令行工具。支持按键驱动快捷菜单，以及 dtmls_cli 空格命令 空格参数 直达执行。',
    )
    parser.add_argument('args', nargs='*', help='留空进入交互模式，也可直接传命令和参数，例如 students stats')
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    ini_path = get_runtime_base_dir() / INI_FILE_NAME

    try:
        app_config = AppConfig.load(ini_path)
        shell = DtmlsShell(app_config)

        if not args.args:
            return shell.run_repl()

        direct_parts = list(args.args)
        raw = ' '.join(direct_parts)
        legacy = parse_inline_legacy_command(raw)
        if legacy is not None:
            command, value = legacy
            if command == 'delete':
                return shell.db_cli.delete_student(value)
            if command == 'show':
                return shell.show_student(value)

        return shell.execute_parts(direct_parts)
    except FileNotFoundError as exc:
        print(str(exc))
        return 3
    except KeyboardInterrupt:
        print('\n操作已中断。')
        return 130
    except Exception as exc:
        print(f'执行失败: {exc}')
        return 1


if __name__ == '__main__':
    sys.exit(main())