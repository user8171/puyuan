import smtplib
import json
import random
from .models import *
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.http.response import JsonResponse

class Smtp:
    def send_email(self, target_email, message):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("arsf32300@gmail.com", "beswcuknwwpmycpd")
        status = server.sendmail(
            "arsf32300@gmail.com", target_email, message)
        server.quit()
        return status


# 1. 註冊
@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        body_data = json.loads(request.body)
        email = body_data["email"]
        password = body_data["password"]
        
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        user_data(password=make_password(password),
            email=email,
            account=email,
            email_verified=0,
            invite_code=generate_invite_code(),
            created_at=time_now,
            updated_at=time_now
        ).save()
        get_user_data_id = user_data.objects.filter(email=email).values()[0]["id"]
        validation(email=email).save()
        user_default(
            user_id=get_user_data_id, 
            created_at=time_now,
            updated_at=time_now
        ).save()
        user_settings(
            user_id=get_user_data_id,
            created_at=time_now
        ).save()
        user_medical(
            user_id=get_user_data_id,
            created_at=time_now
        ).save()
        user_vip(
            id=get_user_data_id,
            created_at=time_now,
            updated_at=time_now
        ).save()
        output = {"status": "0", "message": "成功"}
    return JsonResponse(output, safe=False)

def generate_invite_code():
    invite_code = random.randint(1111111, 9999999)
    while (user_data.objects.filter(invite_code=invite_code).exists()):
        invite_code = random.randint(1111111, 9999999)
    return invite_code

# 2. 登入
@csrf_exempt
def auth(request):
    if request.method == 'POST':
        body_data = json.loads(request.body)
        try:
            data = user_data.objects.filter(email=body_data['email']).values()[0]
            if data['email'] == body_data['email'] and check_password(body_data['password'], data['password']):
                if data['email_verified'] == 0:
                    return JsonResponse({"status": "2", "message": "失敗"}, safe=False)
                request.session.create()
                request.session['id'] = data['id']
                request.session.save()
                login_times = user_data.objects.filter(id=data["id"])
                login_times.update(login_times=login_times.values()[0]['login_times']+1)
                output = {
                    "status": "0",
                    "message": "成功",
                    "token": request.session.session_key
                }
            else:
                output = {"status": "1", "message": "失敗", "token": ""}
        except IndexError:
            output = {"status": "1", "message": "失敗", "token": ""}
    return JsonResponse(output, safe=False)

# 3. 發送驗證碼
@csrf_exempt
def send_validate_code(request):
    if request.method == 'POST':
        body_data = json.loads(request.body)
        email = body_data["email"]

        if not validation.objects.filter(email=email).exists():
            output = {"status": "1", "message": "失敗"}

        random_code = get_random_string(length=6)

        validation.objects.filter(email=email).update(
            code=random_code,
            expire_time=(datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S.%f")
        )
        
        msg = (
            "Subject:註冊驗證碼\n\n驗證碼為: " + 
            random_code +
            "\n驗證碼時效只有10分鐘,時間到後將失效😃😃"
        ).encode('utf-8')

        if Smtp().send_email(email, msg):
            output = {"status": "1", "message": "失敗"}
        else:
            output = {"status": "0", "message": "成功"}
    return JsonResponse(output, safe=False)

# 4. 驗證驗證碼
@csrf_exempt
def validate_code(request):
    if request.method == "POST":
        body_data = json.loads(request.body)
        email = body_data["email"]
        code = body_data["code"]

        get_expire_time = validation.objects.filter(
            email=email).values('expire_time')[0]['expire_time']

        if datetime.now() > get_expire_time:
            return JsonResponse({"status": "1", "message": "失敗"}, safe=False)
        
        get_code = validation.objects.filter(email=email, code=code)
        if get_code != None:
            user_data.objects.filter(
                id=validation.objects.filter(email=email).values()[0]['id']
            ).update(email_verified=1)
            get_code.update(code=None, expire_time=None)
            output = {"status": "0", "message": "成功"}
        else:
            output = {"status": "1", "message": "失敗"}
    return JsonResponse(output, safe=False)

# 5. 忘記密碼
@csrf_exempt
def forgot_password(request):
    if request.method == "POST":
        email = json.loads(request.body)["email"]

        if user_data.objects.filter(email=email).exists():
            new_password = get_random_string(length=8)
            user_data.objects.filter(email=email).update(
                password=make_password(new_password),
                must_change_password=1
            )

            msg = ("Subject:忘記密碼\n\n密碼將被更改為: " + new_password).encode('utf-8')
            if Smtp().send_email(email, msg):
                output = {"status": "1", "message": "失敗"}
            else:
                output = {"status": "0", "message": "成功"}
        else:
            output = {"status": "1", "message": "失敗"}
    return JsonResponse(output, safe=False)

# 6. 重設密碼
@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        password = json.loads(request.body)['password']

        token = request.headers.get('Authorization').split(" ")[1]
        
        id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
        if user_data.objects.filter(id=id).exists():
            user_data.objects.filter(id=id).update(
                password=make_password(password), must_change_password=0
            )
            output = {"status": "0", "message": "成功"}
        else:
            output = {"status": "1", "message": "失敗"}
    return JsonResponse(output, safe=False)

# 38. 註冊確認
@csrf_exempt
def register_validate(request):
    if request.method == "GET":
        email = request.GET.get('email')

        if user_data.objects.filter(email=email).exists():
            output = {"status": "1", "message": "失敗"}
        else:
            output = {"status": "0", "message": "成功"}

    return JsonResponse(output, safe=False)

# 24-1. 分享(POST)
@csrf_exempt
def share_post(request):
    if request.method == "POST":
        data = json.loads(request.body)

        token = request.headers.get('Authorization').split(" ")[1]
        
        get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
        user_share.objects.create(
            user_id=get_id,
            type=data["type"],
            row_id=data["id"],
            relation_type=data["relation_type"]
        )
        output = {"status": "0", "message": "成功"}

    return JsonResponse(output, safe=False)

# 24-2. 查看分享(GET)
def share_get(request, type):
    if request.method == "GET":
        output = {
            "status": "0",
            "message": "成功",
            "records": []
        }
        get_share_data = user_share.objects.filter(
            relation_type=request.get_full_path().split("/")[3]
        ).values()
        for row in get_share_data:
            if row["type"] == 0: # pressure
                get_data = user_blood_pressure.objects.filter(id=row["row_id"]).values()
                get_user_data = user_data.objects.filter(id=get_data[0]["user_id"]).values()[0]
                
                for data in get_data:
                    output["records"].append(
                        {
                            "id": data["id"],
                            "user_id": data["user_id"],
                            "systolic": data["systolic"],
                            "diastolic": data["diastolic"],
                            "pulse": data["pulse"],
                            "created_at": datetime.strftime(data["created_at"], "%Y-%m-%d %H:%M:%S"),
                            "recorded_at": datetime.strftime(data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                            "type": 0,
                            "relation_type": row["relation_type"],
                            "relation_id": 1,
                            
                            "weight": 0,
                            "body_fat": 0,
                            "bmi": 0,
                            "sugar": 0, 
                            "exercise": 0,
                            "drug": 0,
                            "timeperiod": 0,
                            "description": "",
                            "meal": 0,
                            "tag": [[""]],
                            "url": "https://hackmd.io/_uploads/rJzUgN5jh.png",
                            "message": "",
                            "image": [""],
                            "location": {
                                "lat": "",
                                "lng": ""
                            },
                            "reply": "",
                            "user":{
                                "id": get_user_data["id"],
                                "name": get_user_data["name"],
                                "account": get_user_data["account"],
                                "email": get_user_data["email"],
                                "phone": get_user_data["phone"],
                                "fb_id": "fb_" + str(get_user_data["id"]),
                                "status": get_user_data["status"],
                                "group": get_user_data["group"],
                                "birthday": datetime.strftime(get_user_data["birthday"], "%Y-%m-%d"),
                                "height": get_user_data["height"],
                                "gender": get_user_data["gender"],
                                "unread_records": [0, 0, 0],
                                "verified": get_user_data["email_verified"],
                                "privacy_policy": 1,
                                "must_change_password": get_user_data["must_change_password"],
                                "badge": get_user_data["badge"],
                                "created_at": datetime.strftime(get_user_data["created_at"], "%Y-%m-%d %H:%M:%S"),
                                "updated_at": datetime.strftime(get_user_data["updated_at"], "%Y-%m-%d %H:%M:%S")
                            }
                        }
                    )
            elif row["type"] == 1: # weight
                get_data = user_weight.objects.filter(id=row["row_id"]).values()
                get_user_data = user_data.objects.filter(id=get_data[0]["user_id"]).values()[0]
                for data in get_data:
                    output["records"].append(
                        {
                            "id": data["id"],
                            "user_id": data["user_id"],
                            "weight": data["weight"],
                            "body_fat": data["body_fat"],
                            "bmi": data["bmi"],
                            "created_at": datetime.strftime(data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                            "recorded_at": datetime.strftime(data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                            "type": 1,
                            "relation_type": row["relation_type"],
                            "relation_id": 1,
                            
                            "systolic": 0,
                            "diastolic": 0,
                            "pulse": 0,
                            "sugar": 0, 
                            "exercise": 0,
                            "drug": 0,
                            "timeperiod": 0,
                            "description": "",
                            "meal": 0,
                            "tag": [['']],
                            "url": "https://hackmd.io/_uploads/rJzUgN5jh.png",
                            "message": "",
                            "image": [""],
                            "location": {
                                "lat": "",
                                "lng": ""
                            },
                            "reply": "",
                            "user":{
                                "id": get_user_data["id"],
                                "name": get_user_data["name"],
                                "account": get_user_data["account"],
                                "email": get_user_data["email"],
                                "phone": get_user_data["phone"],
                                "fb_id": "fb_" + str(get_user_data["id"]),
                                "status": get_user_data["status"],
                                "group": get_user_data["group"],
                                "birthday": datetime.strftime(get_user_data["birthday"], "%Y-%m-%d"),
                                "height": get_user_data["height"],
                                "gender": get_user_data["gender"],
                                "unread_records": [0, 0, 0],
                                "verified": get_user_data["email_verified"],
                                "privacy_policy": 1,
                                "must_change_password": get_user_data["must_change_password"],
                                "badge": get_user_data["badge"],
                                "created_at": datetime.strftime(get_user_data["created_at"], "%Y-%m-%d %H:%M:%S"),
                                "updated_at": datetime.strftime(get_user_data["updated_at"], "%Y-%m-%d %H:%M:%S")
                            }
                        }
                    )
            elif row["type"] == 2: # sugar
                print(row["row_id"])
                get_data = user_blood_sugar.objects.filter(id=row["row_id"]).values()
                get_user_data = user_data.objects.filter(id=get_data[0]["user_id"]).values()[0]
                for data in get_data:
                    output["records"].append(
                        {
                            "id": data["id"],
                            "user_id": data["user_id"],
                            "sugar": data["sugar"],
                            "exercise": data["exercise"],
                            "drug": data["drug"],
                            "timeperiod": data["time_period"],
                            "created_at": datetime.strftime(data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                            "recorded_at": datetime.strftime(data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                            "type": 2,
                            "relation_type": row["relation_type"],
                            "relation_id": 1,
                            
                            "systolic": 0,
                            "diastolic": 0,
                            "pulse": 0,
                            
                            "weight": 0,
                            "body_fat": 0,
                            "bmi": 0,
                            "description": "",
                            "meal": 0,
                            "tag": [[""]],
                            "url": "https://hackmd.io/_uploads/rJzUgN5jh.png",
                            "message": "",
                            "image": [""],
                            "location": {
                                "lat": "",
                                "lng": ""
                            },
                            "reply": "",
                            "user": {
                                "id": get_user_data["id"],
                                "name": get_user_data["name"],
                                "account": get_user_data["account"],
                                "email": get_user_data["email"],
                                "phone": get_user_data["phone"],
                                "fb_id": "fb_" + str(get_user_data["id"]),
                                "status": get_user_data["status"],
                                "group": get_user_data["group"],
                                "birthday": datetime.strftime(get_user_data["birthday"], "%Y-%m-%d"),
                                "height": get_user_data["height"],
                                "gender": get_user_data["gender"],
                                "unread_records": [0, 0, 0],
                                "verified": get_user_data["email_verified"],
                                "privacy_policy": 1,
                                "must_change_password": get_user_data["must_change_password"],
                                "badge": get_user_data["badge"],
                                "created_at": datetime.strftime(get_user_data["created_at"], "%Y-%m-%d %H:%M:%S"),
                                "updated_at": datetime.strftime(get_user_data["updated_at"], "%Y-%m-%d %H:%M:%S")
                            }
                        }
                    )
            elif row["type"] == 3: # diet
                get_data = user_diary.objects.filter(id=row["row_id"]).values()
                get_user_data = user_data.objects.filter(id=get_data[0]["user_id"]).values()[0]
                for data in get_data:
                    output["records"].append(
                        {
                            "id": data["id"],
                            "user_id": data["user_id"],
                            "description": data["description"],
                            "meal": get_data["meal"],
                            "drug": get_data["drug"],
                            "tag": json.loads(data["tag"]),
                            "url": "https://hackmd.io/_uploads/rJzUgN5jh.png",
                            "message": "",
                            "image": list(data["image"]),
                            "location": {
                                "lat": str(data["lat"]),
                                "lng": str(data["lng"])
                            },
                            "reply": "",
                            "created_at": datetime.strftime(data["created_at"], "%Y-%m-%d %H:%M:%S"),
                            "recorded_at": datetime.strftime(data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                            "type": 3,
                            "relation_type": row["relation_type"],
                            "relation_id": 1,
                            
                            "systolic": 0,
                            "diastolic": 0,
                            "pulse": 0,
                            "weight": 0,
                            "body_fat": 0,
                            "bmi": 0,
                            "sugar": 0, 
                            "exercise": 0,
                            "drug": 0,
                            "timeperiod": 0,
                            "user":{
                                "id": get_user_data["id"],
                                "name": get_user_data["name"],
                                "account": get_user_data["account"],
                                "email": get_user_data["email"],
                                "phone": get_user_data["phone"],
                                "fb_id": "fb_" + str(get_user_data["id"]),
                                "status": get_user_data["status"],
                                "group": get_user_data["group"],
                                "birthday": datetime.strftime(get_user_data["birthday"], "%Y-%m-%d"),
                                "height": get_user_data["height"],
                                "gender": get_user_data["gender"],
                                "unread_records": [0, 0, 0],
                                "verified": get_user_data["email_verified"],
                                "privacy_policy": 1,
                                "must_change_password": get_user_data["must_change_password"],
                                "badge": get_user_data["badge"],
                                "created_at": datetime.strftime(get_user_data["created_at"], "%Y-%m-%d %H:%M:%S"),
                                "updated_at": datetime.strftime(get_user_data["updated_at"], "%Y-%m-%d %H:%M:%S")
                            }
                        }
                )
    return JsonResponse(output, safe=False)

# 29. 最新消息
@csrf_exempt
def news_(request):
    if request.method == "GET":
        output = {
            "status": "0",
            "message": "成功",
            "news": []
        }
        try:
            get_data = news.objects.all().values()
            for data in get_data:
                output["news"].append({
                    "id": data["id"],
                    "member_id": data["member_id"],
                    "group": data["group"],
                    "message": data["message"],
                    "pushed_at": datetime.strftime(data["pushed_at"], "%Y-%m-%d %H:%M:%S"),
                    "created_at": datetime.strftime(data["created_at"], "%Y-%m-%d %H:%M:%S"),
                    "updated_at": datetime.strftime(data["updated_at"], "%Y-%m-%d %H:%M:%S")
                })
        except:
            output = {"status": "1", "message": "失敗"}
    return JsonResponse(output, safe=False)
    