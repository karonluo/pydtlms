import ast
for p in [
    r'D:\pyproj\pydtlms\backend\app\schemas\student.py',
    r'D:\pyproj\pydtlms\backend\app\schemas\portal.py',
    r'D:\pyproj\pydtlms\backend\app\api\v1\students.py',
    r'D:\pyproj\pydtlms\backend\app\services\management_service_students.py',
    r'D:\pyproj\pydtlms\backend\app\services\management_service_research_centers.py',
    r'D:\pyproj\pydtlms\backend\app\services\management_service_core.py',
    r'D:\pyproj\pydtlms\backend\app\services\postgres_state_store_core.py',
    r'D:\pyproj\pydtlms\backend\app\services\postgres_state_store_query_students.py',
    r'D:\pyproj\pydtlms\backend\app\services\postgres_state_store_query_recruitment.py',
    r'D:\pyproj\pydtlms\backend\app\services\postgres_state_store_sync.py',
]:
    try:
        with open(p, encoding='utf-8') as f:
            ast.parse(f.read(), filename=p)
        print('OK:', p)
    except SyntaxError as e:
        print('SYNTAX ERROR:', p, '->', e)
