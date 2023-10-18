import json
from login.models import *
from datetime import datetime
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.db.models import Q

# 16. 獲取控糖團邀請碼
@csrf_exempt
def get_invite_code(request):
    if request.method == "GET":
        token = request.headers.get('Authorization').split(" ")[1]
        get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
        output = {
            "status": "0", 
            "message": "成功", 
            "invite_code": user_data.objects.filter(id=get_id).values()[0]["invite_code"]
        }
    return JsonResponse(output, safe=False)

# 17. 控糖團列表
@csrf_exempt
def get_friend_list(request):
    if request.method == "GET":
        token = request.headers.get('Authorization').split(" ")[1]
        
        get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
        friend_list = user_friend.objects.filter(Q(receiver_id=get_id) | Q(sender_id=get_id)).values()
        output = {
            "status": "0",
            "message": "成功",
            "friends": []
        }
        if len(friend_list) != 0:
            for data in friend_list:
                friend_id = data["sender_id"] if data["sender_id"] != get_id else data["receiver_id"]
                get_user_data = user_data.objects.filter(
                    id=friend_id
                ).values()[0]
                output["friends"].append({
                    "id": friend_id,
                    "name": get_user_data["name"],
                    "relation_type": data["type"]
                })
        else:
            output["friends"] = [{
                "id": -1,
                "name": "none",
                "relation_type": 0
            }]
    return JsonResponse(output, safe=False)

# 18. 獲取控糖團邀請
@csrf_exempt
def get_friend_requests(request):
    if request.method == "GET":
        output = {
            "status": "0",
            "message": "成功",
            "requests": []
        }
        for req in user_friend.objects.filter(
            receiver_id=Session.objects.filter(
                session_key=request.headers.get('Authorization').split(" ")[1]
            )[0].get_decoded()['id'], 
            status=0
        ).values():
            get_data = user_data.objects.filter(id=req["sender_id"]).values()[0]
            output["requests"].append({
                "id": req["id"],
                "user_id": req["sender_id"],
                "relation_id": req["sender_id"],
                "type": req["type"],
                "status": req["status"],
                "read": req["read"],
                "created_at": datetime.strftime(req["created_at"], "%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.strftime(req["updated_at"], "%Y-%m-%d %H:%M:%S"),
                "user": {
                    "id": get_data["id"],
                    "name": get_data["name"],
                    "account": "fb_" + str(get_data["id"])
                }
            })
    return JsonResponse(output, safe=False)

# 19. 送出控糖團邀請
@csrf_exempt
def send_request(request):
    if request.method == "POST":
        body_data = json.loads(request.body)
        
        receiver_id = user_data.objects.filter(
            invite_code=body_data["invite_code"]
        )
        sender_id = Session.objects.filter(
            session_key=request.headers.get('Authorization').split(" ")[1]
        )[0].get_decoded()['id']
        
        if receiver_id == None or sender_id == receiver_id:
            return JsonResponse({"status": "1", "message": "失敗"}, safe=False)

        receiver_id = receiver_id.values()[0]["id"]
        if user_friend.objects.filter(Q(
            sender_id=sender_id,
            receiver_id=receiver_id
        )| Q(
            sender_id=receiver_id,
            receiver_id=sender_id
        )
        ).exists():
            return JsonResponse({"status": "2", "message": "失敗"}, safe=False)

        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        user_friend.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            type=body_data["type"],
            status=0,
            created_at=time_now,
            updated_at=time_now
        )

        output = {"status": "0", "message": "成功"}
    return JsonResponse(output, safe=False)

# 20. 接受控糖團邀請, 21.拒絕控糖團邀請
#好友列表跟好友邀請列表合一起
@csrf_exempt
def process_request(request, code, state):
    if request.method == "GET":
        token = request.headers.get('Authorization').split(" ")[1]
        
        if state == 'accept':
            receiver_id = Session.objects.filter(session_key=token)[0].get_decoded()["id"]
            sender_id = user_friend.objects.filter(receiver_id=receiver_id).order_by("status").values()[0]["sender_id"]
            user_friend.objects.filter(
                receiver_id=receiver_id, 
                sender_id=sender_id
            ).update(
                status=1,
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            )
        elif state == "refuse":
            receiver_id = user_data.objects.filter(
                id=code
            ).values()[0]["id"]
            sender_id = Session.objects.filter(session_key=token)[0].get_decoded()["id"]
            user_friend.objects.filter(receiver_id=receiver_id, sender_id=sender_id).delete()

        output = {"status": "0", "message": "成功"}
    return JsonResponse(output, safe=False)

# 26. 控糖團結果
@csrf_exempt
def friend_results(request):
    if request.method == "GET":
        token = request.headers.get('Authorization').split(" ")[1]
        
        get_id = Session.objects.filter(session_key=token)[0].get_decoded()['id']
        friend_result = user_friend.objects.filter(Q(sender_id=get_id) | Q(receiver_id=get_id), status=1, read=0).values()

        output = {
            "status": "0",
            "message": "成功", 
            "results": []
        }
        for index in friend_result:
            friend_data = user_data.objects.filter(
                id=index["receiver_id"] if index["receiver_id"] != get_id else index["sender_id"]
            ).values()[0]
            output["results"].append(
                {
                    "id": index["id"],
                    "user_id": index["sender_id"],
                    "relation_id": index["receiver_id"],
                    "type": index["type"],
                    "status": index["status"],
                    "read": index["read"],
                    "created_at": datetime.strftime(index["created_at"], "%Y-%m-%d %H:%M:%S"),
                    "updated_at": datetime.strftime(index["updated_at"], "%Y-%m-%d %H:%M:%S"),
                    "relation": {
                        "id": friend_data["id"],
                        "name": friend_data["name"],
                        "account": "fb_" + str(friend_data["id"])
                    }
                }
            )
            user_friend.objects.filter(
                sender_id=get_id,
                status=1,
                read=0
            ).update(
                read=1
            )
    return JsonResponse(output, safe=False)

# 37. 刪除更多好友
@csrf_exempt
def friend_delete(request):
    if request.method == "DELETE":
        get_id = Session.objects.filter(
            session_key=request.headers.get('Authorization').split(" ")[1]
        )[0].get_decoded()['id']
        del_id = json.loads(request.body)["ids[]"]
        try:
            user_friend.objects.filter(
                Q(sender_id=get_id, receiver_id=del_id) | 
                Q(sender_id=del_id, receiver_id=get_id)
            ).delete()
            output = {"status": "0", "message": "成功"}
        except:
            output = {"status": "1", "message": "失敗"}
    return JsonResponse(output, safe=False)
