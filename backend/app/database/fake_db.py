from ..core.security import get_password_hash

fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "hashed_password": get_password_hash("123456"),  # mật khẩu 123456 đã hash
        "disabled": False,
    }
}