from app.core.security import authenticate_system_user
candidates = ['ChangeMe@123', 'Admin@123456', 'zhangweinan@123', 'ZhangWeinan@123', 'ChangeMe123', 'ChangeMe@2026']
for pw in candidates:
    try:
        user = authenticate_system_user('zhangweinan', pw)
        print(pw, '=>', bool(user), user.get('username') if user else None)
    except Exception as exc:
        print(pw, '=> ERROR', type(exc).__name__, exc)
