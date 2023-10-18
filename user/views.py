import json
from login.models import *
from datetime import datetime
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

# 7. 使用者資料 、 12. 個人資訊
@csrf_exempt
def profile_setting(request):
    if request.method == "PATCH":
        token = request.headers.get('Authorization').split(" ")[1]
        
        body_data = json.loads(request.body)
        body_data["weight"] = 0

        get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
        update_data = user_data.objects.filter(id=get_id)        
        for i in body_data:
            if body_data[i] == "":
                continue
            update_data.update(**{i: body_data[i]}, updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        output = {"status": "0", "message": "成功"}

    if request.method == "GET":
        token = request.headers.get('Cookie').split(" ")[1]
        
        try:
            get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
            user_data_data = user_data.objects.filter(id=get_id).values()[0]
            user_default_data = user_default.objects.filter(id=get_id).values()[0]
            user_settings_data = user_settings.objects.filter(id=get_id).values()[0]
            user_vip_data = user_vip.objects.filter(id=get_id).values()[0]
            output = {
                "status": "0",
                "message": "成功",
                "user": {
                    "id": user_data_data["id"],
                    "name": user_data_data["name"],
                    "account": user_data_data["account"],
                    "email": user_data_data["email"],
                    "phone": user_data_data["phone"],
                    "fb_id": "未設置",
                    "status": user_data_data["status"],
                    "group": user_data_data["group"],
                    "birthday": datetime.strftime(user_data_data["birthday"], "%Y-%m-%d %H:%M:%S"),
                    "height": user_data_data["height"],
                    "weight": user_data_data["weight"],
                    "gender": user_data_data["gender"],
                    "address": user_data_data["address"],
                    "unread_records": [0, 0, 0],
                    "verified": user_data_data["email_verified"],
                    "privacy_policy": 1,
                    "must_change_password": int(user_data_data["must_change_password"]),
                    "fcm_id": user_data_data["fcm_id"],
                    "badge": user_data_data["badge"],
                    "login_times": user_data_data["login_times"],
                    "created_at": datetime.strftime(user_data_data["created_at"], "%Y-%m-%d %H:%M:%S"),
                    "updated_at": datetime.strftime(user_data_data["updated_at"], "%Y-%m-%d %H:%M:%S"),
                    "default": {
                        "id": user_data_data["id"],
                        "user_id": user_default_data["id"],
                        "sugar_delta_max": user_default_data["sugar_delta_max"],
                        "sugar_delta_min": user_default_data["sugar_delta_min"],
                        "sugar_morning_max": user_default_data["sugar_morning_max"],
                        "sugar_morning_min": user_default_data["sugar_morning_min"],
                        "sugar_evening_max": user_default_data["sugar_evening_max"],
                        "sugar_evening_min": user_default_data["sugar_evening_min"],
                        "sugar_before_max": user_default_data["sugar_before_max"],
                        "sugar_before_min": user_default_data["sugar_before_min"],
                        "sugar_after_max": user_default_data["sugar_after_max"],
                        "sugar_after_min": user_default_data["sugar_after_min"],
                        "systolic_max": user_default_data["systolic_max"],
                        "systolic_min": user_default_data["systolic_min"],
                        "diastolic_max": user_default_data["diastolic_max"],
                        "diastolic_min": user_default_data["diastolic_min"],
                        "pulse_max": user_default_data["pulse_max"],
                        "pulse_min": user_default_data["pulse_min"],
                        "weight_max": user_default_data["weight_max"],
                        "weight_min": user_default_data["weight_min"],
                        "bmi_max": user_default_data['bmi_max'],
                        "bmi_min": user_default_data["bmi_min"],
                        "body_fat_max": user_default_data["body_fat_max"],
                        "body_fat_min": user_default_data["body_fat_min"],
                        "created_at": datetime.strftime(user_default_data["created_at"], "%Y-%m-%d %H:%M:%S"),
                        "updated_at": datetime.strftime(user_default_data["updated_at"], "%Y-%m-%d %H:%M:%S")
                    },
                    "setting": {
                        "id": user_settings_data["id"],
                        "user_id": user_data_data["id"],
                        "after_recording": int(user_settings_data["after_recording"]),
                        "no_recording_for_a_day": int(user_settings_data["no_recording_for_a_day"]),
                        "over_max_or_under_min": int(user_settings_data["over_max_or_under_min"]),
                        "after_meal": int(user_settings_data["after_meal"]),
                        "unit_of_sugar": int(user_settings_data["unit_of_sugar"]),
                        "unit_of_weight": int(user_settings_data["unit_of_weight"]),
                        "unit_of_height": int(user_settings_data["unit_of_height"]),
                        "created_at": datetime.strftime(user_data_data["created_at"], "%Y-%m-%d %H:%M:%S"),
                        "updated_at": datetime.strftime(user_settings_data["updated_at"], "%Y-%m-%d %H:%M:%S")
                    },
                    "vip": {
                        "id": user_data_data["id"],
                        "user_id": user_vip_data["id"],
                        "level": user_vip_data["level"],
                        "remark": user_vip_data["remark"],
                        "started_at": datetime.strftime(user_vip_data["started_at"], "%Y-%m-%d %H:%M:%S"),
                        "ended_at": datetime.strftime(user_vip_data["ended_at"], "%Y-%m-%d %H:%M:%S"),
                        "created_at": datetime.strftime(user_vip_data["created_at"], "%Y-%m-%d %H:%M:%S"),
                        "updated_at": datetime.strftime(user_vip_data["updated_at"], "%Y-%m-%d %H:%M:%S")
                    }
                }
            }
        except:
            output = {"status": "1", "message": "失敗"}
    return JsonResponse(output, safe=False)

# 8. 上傳血壓測量結果
@csrf_exempt
def update_pressure(request):
    if request.method == "POST":
        token = request.headers.get('Authorization').split(" ")[1]

        body_data = json.loads(request.body)
        try:
            get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
            user_blood_pressure.objects.create(
                user_id=get_id,
                systolic=body_data["systolic"],
                diastolic=body_data["diastolic"],
                pulse=body_data["pulse"],
                recorded_at=body_data["recorded_at"]
            )
            output = {"status": "0", "message": "成功"}
        except:
            output = {"status": "1", "message": "失敗"}
    return JsonResponse(output, safe=False)

# 9. 上傳體重測量結果
@csrf_exempt
def update_weight(request):
    if request.method == "POST":
        token = request.headers.get('Authorization').split(" ")[1]

        body_data = json.loads(request.body)
        try:
            get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
            user_weight.objects.create(
                user_id=get_id,
                weight=body_data["weight"],
                body_fat=body_data["body_fat"],
                bmi=body_data["bmi"],
                recorded_at=body_data["recorded_at"]
            )
            output = {"status": "0", "message": "成功"}
        except:
            output = {"status": "1", "message": "失敗"}
    return JsonResponse(output, safe=False)

# 10. 上傳血糖
@csrf_exempt
def update_sugar(request):
    if request.method == "POST":
        token = request.headers.get('Authorization').split(" ")[1]
        
        body_data = json.loads(request.body)
        try:
            get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
            user_blood_sugar.objects.create(
                user_id=get_id,
                sugar=body_data["sugar"],
                time_period=body_data["timeperiod"],
                recorded_at=body_data["recorded_at"],
                drug=body_data["drug"],
                exercise=body_data["exercise"]
            )
            output = {"status": "0", "message": "成功"}
        except:
            output = {"status": "1", "message": "失敗"}
    return JsonResponse(output, safe=False)

# 11. 個人預設值
@csrf_exempt
def user_default_settings(request):
    if request.method == "PATCH":
        body_data = json.loads(request.body)
        get_id = Session.objects.filter(
            session_key=request.headers.get('Authorization').split(" ")[1]
        )[0].get_decoded()['id']
        for i in body_data:
            user_default.objects.filter(id=get_id).update(
                **{i: body_data[i]},
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            )
        output = {"status": "0", "message": "成功"}
    return JsonResponse(output, safe=False)

# 14. 個人日誌列表
@csrf_exempt
def user_diary_(request):
    if request.method == "GET":
        token = request.headers.get('Authorization').split(" ")[1]

        time = request.GET.get('date')
        get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
        output = {
            "status": "0",
            "message": "成功",
            "diary": []
        }

        data = user_blood_pressure.objects.filter(
            user_id=get_id,
            recorded_at__date=time
        ).values()
        if len(data) != 0:
            for index_data in data:
                output["diary"].append(
                    {
                        "id": index_data["id"],
                        "user_id": index_data["user_id"],
                        "systolic": index_data["systolic"],
                        "diastolic": index_data["diastolic"],
                        "pulse": index_data["pulse"],
                        "recorded_at": datetime.strftime(index_data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                        "type": "blood_pressure",
                        
                        "weight": 0,
                        "body_fat": 0,
                        "bmi": 0,
                        "sugar": 0,
                        "exercise": 0,
                        "drug": 0,
                        "timeperiod": 0,
                        "description": "",
                        "meal": 0,
                        "tag": [{"name": [""], "message": ""}],
                        "image": [""],
                        "location": {
                            "lat": "",
                            "lng": ""
                        },
                        "reply": ""                      
                    }
                )

        data = user_weight.objects.filter(
            user_id=get_id,
            recorded_at__date=time
        ).values()
        if len(data) != 0:
            for index_data in data:
                output["diary"].append(
                    {
                        "id": index_data["id"],
                        "user_id": index_data["user_id"],
                        "weight": index_data["weight"],
                        "body_fat": index_data["body_fat"],
                        "bmi": index_data["bmi"],
                        "recorded_at": datetime.strftime(index_data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                        "type": "weight",
                        
                        "systolic": 0,
                        "diastolic": 0,
                        "pulse": 0,
                        "sugar": 0,
                        "exercise": 0,
                        "drug": 0,
                        "timeperiod": 0,
                        "description": "",
                        "meal": 0,
                        "tag": [{"name": [""], "message": ""}],
                        "image": [""],
                        "location": {
                            "lat": "",
                            "lng": ""
                        },
                        "reply": "" 
                    }
                )

        data = user_blood_sugar.objects.filter(
            user_id=get_id,
            recorded_at__date=time
        ).values()
        if len(data) != 0:
            for index_data in data:
                output["diary"].append(
                    {
                        "id": index_data["id"],
                        "user_id": index_data["user_id"],
                        "sugar": index_data["sugar"],
                        "exercise": index_data["exercise"],
                        "drug": index_data["drug"],
                        "timeperiod": index_data["time_period"],
                        "recorded_at": datetime.strftime(index_data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                        "type": "blood_sugar",
                        
                        "systolic": 0,
                        "diastolic": 0,
                        "pulse": 0,
                        
                        "weight": 0,
                        "body_fat": 0,
                        "bmi": 0,
                        "description": "",
                        "meal": 0,
                        "tag": [{"name": [""], "message": ""}],
                        "image": [""],
                        "location": {
                            "lat": "",
                            "lng": ""
                        },
                        "reply": ""
                    }
                )

        data = user_diary.objects.filter(
            user_id=get_id,
            recorded_at__date=time
        ).values()
        if len(data) != 0:
            for index_data in data:
                index_data["tag"] = index_data["tag"].replace("'", '"')
                output["diary"].append(
                    {
                        "id": index_data["id"],
                        "user_id": index_data["user_id"],
                        "description": index_data["description"],
                        "meal": index_data["meal"],
                        "tag": eval(index_data["tag"]),
                        # "image": list(index_data["image"]),
                        "image": [],
                        "location": {
                            "lat": str(index_data["lat"]),
                            "lng": str(index_data["lng"])
                        },
                        "reply": "",
                        "recorded_at": datetime.strftime(index_data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                        "type": "diet",
                        
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
                    }
                )
    return JsonResponse(output, safe=False)

# 15. 飲食日記
@csrf_exempt
def user_diet_(request):
    if request.method == "POST":
        token = request.headers.get('Authorization').split(" ")[1]
        
        data = json.loads(request.body)

        get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
        tag_data = []
        
        for message in data["tag[]"]:
            tag_data.append({
                "name": [user_data.objects.filter(id=get_id).values()[0]["name"]],
                "message": message
            })
        user_diary.objects.create(
            user_id=get_id,
            description=data["description"],
            meal=data["meal"],
            tag=str(tag_data),
            image=str(data["image"]),
            lat=data["lat"],
            lng=data["lng"],
            recorded_at=data["recorded_at"]
        )
        output = {
            "status": "0",
            "message": "成功", 
            "image_url": "https://hackmd.io/_uploads/rJzUgN5jh.png"
        }
    return JsonResponse(output, safe=False)

# 25. 最後上傳時間
@csrf_exempt
def last_update(request):
    if request.method == "GET":
        token = request.headers.get('Authorization').split(" ")[1]
        

        get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
        output = {
            "status": "0",
            "last_upload": {
            }
        }

        pressure_data = user_blood_pressure.objects.filter(user_id=get_id)
        if pressure_data != None:
            pressure_data = pressure_data.values()[len(pressure_data.values())-1]
            output["last_upload"]["blood_pressure"] = datetime.strftime(pressure_data["recorded_at"], "%Y-%m-%d %H:%M:%S")
        else:
            output["last_upload"]["weight"] = "null"

        weight_data = user_weight.objects.filter(user_id=get_id)
        if weight_data != None:
            weight_data = weight_data.values()[len(weight_data.values())-1]
            output["last_upload"]["weight"] = datetime.strftime(weight_data["recorded_at"], "%Y-%m-%d %H:%M:%S")
        else:
            output["last_upload"]["weight"] = "null"

        sugar_data = user_blood_sugar.objects.filter(user_id=get_id)
        if sugar_data != None:
            sugar_data = sugar_data.values()[len(sugar_data.values())-1]
            output["last_upload"]["blood_sugar"] = datetime.strftime(sugar_data["recorded_at"], "%Y-%m-%d %H:%M:%S")
        else:
            output["last_upload"]["blood_sugar"] = "null"

        diet_data = user_diary.objects.filter(user_id=get_id)
        if diet_data != None:
            diet_data = diet_data.values()[len(diet_data.values())-1]
            output["last_upload"]["diet"] = datetime.strftime(diet_data["recorded_at"], "%Y-%m-%d %H:%M:%S")
        else:
            output["last_upload"]["diet"] = "null"

    return JsonResponse(output, safe=False)

# 27. 獲取關懷諮詢, 28. 發送關懷諮詢
# 28似乎沒有觸發方式
@csrf_exempt
def cares(request):
    if request.method == "GET":
        token = request.headers.get('Authorization').split(" ")[1]
        

        get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
        output = {
            "status": "0",
            "message": "成功",
            "cares": []
        }

        get_data = user_care.objects.filter(user_id=get_id).values()
        for data in get_data:
            output["cares"].append({
                "id": data["id"],
                "user_id": get_id,
                "member_id": 1,
                "reply_id": "",
                "message": data["message"],
                "created_at":  datetime.strftime(data["created_at"], "%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.strftime(data["updated_at"], "%Y-%m-%d %H:%M:%S")
            })

        return JsonResponse(output, safe=False)

    if request.method == "POST":
        token = request.headers.get('Authorization').split(" ")[1]
        
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        user_care.objects.create(
            user_id=get_id,
            message=json.loads(request.body)["message"],
            created_at=time_now,
            updated_at=time_now
        )
        output = {"status": "0", "message": "成功"}
    return JsonResponse(output, safe=False)

# 30. 就醫資訊, 31. 更新就醫資訊
@csrf_exempt
def medical(request):
    if request.method == "GET":       
        get_data = user_medical.objects.filter(
            user_id=Session.objects.filter(
                session_key=request.headers.get('Authorization').split(" ")[1]
            )[0].get_decoded()['id']
        ).values()[0]
        
        output = {
            "status": "0",
            "message": "成功",
            "medical_info": {
                "id": get_data["id"],
                "user_id": get_data["user_id"],
                "diabetes_type": get_data["diabetes_type"],
                "oad": get_data["oad"],
                "insulin": get_data["insulin"],
                "anti_hypertensives": get_data["anti_hypertensives"],
                "created_at": datetime.strftime(get_data["created_at"], "%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.strftime(get_data["updated_at"], "%Y-%m-%d %H:%M:%S")
            }
        }
        
    if request.method == "PATCH":
        data = json.loads(request.body)
        
        for key in json.loads(request.body):
            user_medical.objects.filter(
                user_id=Session.objects.filter(
                    session_key=request.headers.get('Authorization').split(" ")[1]
                )[0].get_decoded()['id']
            ).update(
                **{key: int(data[key])},
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            )
        output = {"status": "0", "message": "成功"}
    return JsonResponse(output, safe=False)

# 32. 糖化血色素, 33. 送糖化血色素, 34. 刪除糖化血色素
@csrf_exempt
def a1c(request):
    if request.method == "GET":      
        try:
            get_data = user_a1c.objects.filter(
                user_id=Session.objects.filter(
                    session_key=request.headers.get('Authorization').split(" ")[1]
                )[0].get_decoded()['id']
            ).values()
        except IndexError:
            return JsonResponse({"status": "1", "message": "失敗"}, safe=False)
        output = {
            "status": "0",
            "message": "成功",
            "a1cs": []
        }
        for data in get_data:   
            output["a1cs"].append({
                "id": data["id"],
                "user_id": data["user_id"],
                "a1c": str(data["a1c"]),
                "recorded_at": datetime.strftime(data["recorded_at"], "%Y-%m-%d %H:%M:%S"),
                "created_at": datetime.strftime(data["created_at"], "%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.strftime(data["updated_at"], "%Y-%m-%d %H:%M:%S")
            })

    if request.method == "POST":
        try:
            get_id = Session.objects.filter(
                session_key=request.headers.get('Authorization').split(" ")[1]
            )[0].get_decoded()['id']
            user_a1c.objects.create(
                user_id=get_id,
                a1c=json.loads(request.body)["a1c"],
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                recorded_at=json.loads(request.body)["recorded_at"]
            )
            output = {"status": "0", "message": "成功"}
        except:
            output = {"status": "1", "message": "失敗"}

    if request.method == "DELETE":
        for index in list(json.loads(request.body)["ids[]"]):
            user_a1c.objects.filter(id=index).delete()
        output = {"status": "0", "message": "成功"}
    return JsonResponse(output, safe=False)

# 35. 個人設定
@csrf_exempt
def settings(request):
    if request.method == "PATCH":
        token = request.headers.get('Authorization').split(" ")[1]
        
        try:
            get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            for data in json.loads(request.body):
                user_settings.objects.filter(user_id=get_id).update(**{data: json.loads(request.body)[data]},
                                                                    updated_at=time_now)
            output = {"status": "0", "message": "成功"}
        except:
            output = {"status": "1", "message": "失敗"}

    return JsonResponse(output, safe=False)

# 39. 更新badge
@csrf_exempt
def update_badge(request):
    if request.method == "PUT":
        get_id = Session.objects.filter(
            session_key=request.headers.get('Authorization').split(" ")[1]
        )[0].get_decoded()['id']
        user_data.objects.filter(id=get_id).update(
            badge=json.loads(request.body)["badge"]
        )
        output = {"status": "0", "message": "成功"}
    return JsonResponse(output, safe=False)

# 40. 刪除日記記錄, 44. 上一筆紀錄資訊
@csrf_exempt
def delete_records(request):
    if request.method == "DELETE":
        body_data = json.loads(request.body)
        for data in body_data['deleteObject']:
            if data == "blood_sugars":
                blood_sugar = body_data['deleteObject']["blood_sugars"]
                for index in blood_sugar:
                    user_blood_sugar.objects.filter(id=index).delete()
            elif data == "blood_pressures":
                blood_pressure = body_data['deleteObject']["blood_pressures"]
                for index in blood_pressure:
                    user_blood_pressure.objects.filter(id=index).delete()
            elif data == "weights":
                weights = body_data['deleteObject']["weights"]
                for index in weights:
                    user_weight.objects.filter(id=index).delete()
            elif data == "diets":
                diets = body_data['deleteObject']["diets"]
                for index in diets:
                    user_diary.objects.filter(id=index).delete()

        output = {"status": "0", "message": "成功"}
        
    if request.method == "POST":
        get_id = Session.objects.filter(
            session_key=request.headers.get('Authorization').split(" ")[1]
        )[0].get_decoded()["id"]

        output = {
            "status": "0",
            "message": "成功",
            "blood_sugars": {
                "sugar": 0
            },
            "blood_pressures": {
                "systolic": 0,
                "diastolic": 0,
                "pulse": 0
            },
            "weights": {
                "weight": 0
            }
        }
        
        data = user_blood_sugar.objects.filter(
            user_id=get_id,
            time_period=json.loads(request.body)["diet"]
        ).order_by("-recorded_at").values()
        if len(data) != 0:
            output["blood_sugars"] = {
                "sugar": data[0]["sugar"]
            }

        data = user_blood_pressure.objects.filter(user_id=get_id).order_by("-recorded_at").values()
        if len(data) != 0:
            output["blood_pressures"] = {
                "systolic": data[0]["systolic"],
                "diastolic": data[0]["diastolic"],
                "pulse": data[0]["pulse"]
            }

        data = user_weight.objects.filter(user_id=get_id).order_by("-recorded_at").values()
        if len(data) != 0:
            output["weights"] = {
                "weight": data[0]["weight"]
            }
    return JsonResponse(output, safe=False)

# 41. (取得)藥物資訊, 42. 上傳藥物資訊, 43. 刪除藥物資訊
@csrf_exempt
def drug_info(request):
    if request.method == "GET":
        output = {
            "status": "0",
            "message": "成功",
            "drug_useds": []
        }
        drug_data = user_drugs.objects.filter(
            user_id=Session.objects.filter(
                session_key=request.headers.get('Authorization').split(" ")[1]
            )[0].get_decoded()['id']
        ).values()
        for data in drug_data:
            output["drug_useds"].append({
                "id": data["id"],
                "user_id": data["user_id"],
                "type": data["type"],
                "name": data["name"],
                "recorded_at": datetime.strftime(data["recorded_at"], ("%Y-%m-%d %H:%M:%S")),
                "updated_at": datetime.strftime(data["updated_at"], "%Y-%m-%d %H:%M:%S"),
                "created_at": datetime.strftime(data["created_at"], "%Y-%m-%d %H:%M:%S")
            })

    if request.method == "POST":  
        get_id = Session.objects.filter(
            session_key=request.headers.get('Authorization').split(" ")[1]
        )[0].get_decoded()['id']
        user_drugs.objects.create(
            user_id=get_id,
            type=json.loads(request.body)["type"],
            name=json.loads(request.body)["name"],
            recorded_at=json.loads(request.body)["recorded_at"],
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        )
        
        output = {"status": "0", "message": "成功"}
            
    if request.method == "DELETE":
        for index in list(json.loads(request.body)["ids[]"]):
            user_drugs.objects.filter(id=index).delete()

        output = {"status": "0", "message": "成功"}
    return JsonResponse(output, safe=False)
