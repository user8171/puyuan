from django.urls import path
from . import views

urlpatterns = [
    # 設定個人資料、(取得)個人資訊
    path("/", views.profile_setting, name="profile_setting_get"),
    path("", views.profile_setting, name="profile_setting_post "),
    # 上傳血壓測量結果
    path("/blood/pressure", views.update_pressure, name="update_pressure"),
    # 上傳體重測量結果
    path("/weight", views.update_weight, name="update_weight"),
    # 上傳血糖
    path("/blood/sugar", views.update_sugar, name="update_sugar"),
    # 個人預設值
    path("/default", views.user_default_settings, name="user_default_settings"),
    # 日記列表資料
    path("/diary", views.user_diary_, name="user_diary_"),
    # 飲食日記
    path("/diet", views.user_diet_, name="user_diet_"),
    # 最後上傳時間
    path("/last-upload", views.last_update, name="last_update"),
    # 獲取關懷諮詢, 發送關懷諮詢
    path("/care", views.cares, name="cares"),
    # 就醫資訊, 更新就醫資訊
    path("/medical", views.medical, name="medical"),
    # (取得)糖化血色素, 送糖化血色素, 刪除糖化血色素
    path("/a1c", views.a1c, name="a1c"),
    # 個人設定
    path("/setting", views.settings, name="settings"),
    # 更新badge
    path("/badge", views.update_badge, name="update_badge"),
    # 刪除日記記錄, 上一筆紀錄資訊
    path("/records", views.delete_records, name="delete_records"),
    # 藥物資訊, 上傳藥物資訊, 刪除藥物資訊
    path("/drug-used", views.drug_info, name="drug_info"),
]