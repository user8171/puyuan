from django.urls import path
from . import views

urlpatterns = [
    # 獲取控糖團邀請碼
    path("/code", views.get_invite_code, name="get_invite_code"),
    # 控糖團列表 
    path("/list", views.get_friend_list, name="get_friend_list"),
    # 獲取控糖團邀請
    path("/requests", views.get_friend_requests, name="get_friend_requests"),
    # 送出控糖團邀請
    path("/send", views.send_request, name="send_request"),
    # 接受控糖團邀請, 拒絕控糖團邀請
    path("/<code>/<state>", views.process_request, name="process_request"),
    # 控糖團結果
    path("/results", views.friend_results, name="friend_results"),
    # 刪除更多好友
    path("/remove", views.friend_delete, name="friend_delete"),
]