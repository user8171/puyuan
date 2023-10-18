from django.urls import path
from . import views

urlpatterns = [
    # 註冊
    path("/register", views.sign_up, name="sign_up"),
    # 登入
    path("/auth", views.auth, name="auth"), 
    # 發送驗證碼
    path("/verification/send", views.send_validate_code, name="send_validate_code"),
    # 驗證驗證碼
    path("/verification/check", views.validate_code, name="validate_code"),
    # 忘記密碼
    path("/password/forgot", views.forgot_password, name="forgot_password"),
    # 重設密碼
    path("/password/reset", views.reset_password, name="reset_password"),
    # 註冊確認
    path("/register/check", views.register_validate, name="register_validate"),
    # 分享     
    path("/share", views.share_post, name="share_post"),
    # 查看分享     
    path("/share/<type>", views.share_get, name="share_get"),
    # 最新消息
    path("/news", views.news_, name="news")
]