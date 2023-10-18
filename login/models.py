from django.db import models
from django import forms

# Create your models here.
class user_data(models.Model):
    account = models.CharField(max_length=30, null=False, default="")
    email = models.CharField(max_length=255, null=False, default="")
    password = models.CharField(max_length=255, null=False, default="")
    login_times = models.IntegerField(null=True, default=0)
    email_verified = models.IntegerField(null=False, default=0)
    must_change_password = models.BooleanField(default=False)
    name = models.CharField(max_length=20, null=True, default="使用者")
    phone = models.CharField(max_length=10, null=True, default="")
    birthday = models.DateField(null=True, default="1920-1-1")
    height = models.FloatField(max_length=3, null=True, default=0)
    weight = models.FloatField(max_length=3, null=True, default=0)
    gender = models.IntegerField(null=True, default=0)
    address = models.CharField(max_length=50, null=True, default="")
    fcm_id = models.CharField(max_length=50, null=True, default="")
    invite_code = models.CharField(max_length=10, null=True, default="0")
    group = models.CharField(max_length=20, null=True, default="")
    status = models.CharField(max_length=10, null=True, default="Normal")
    unread_records = models.CharField(max_length=200, null=True, default="[0, 0, 0]")
    badge = models.IntegerField(null=True, default=0)
    updated_at = models.DateTimeField(null=True, default="1920-1-1")
    created_at = models.DateTimeField(null=True, default="1920-1-1")

class validation(models.Model):
    email = models.CharField(max_length=255, null=False, default="")
    code = models.CharField(max_length=6, null=True, default="0")
    expire_time = models.DateTimeField(null=True, default="1920-1-1")

class user_blood_pressure(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    systolic = models.IntegerField(null=True, default=0)
    diastolic = models.IntegerField(null=True, default=0)
    pulse = models.IntegerField(null=True, default="0")
    recorded_at = models.DateTimeField(null=True, default="1920-1-1")

class user_weight(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    weight = models.FloatField(null=True, default=0)
    body_fat = models.FloatField(null=True, default=0)
    bmi = models.FloatField(null=True, default=0)
    recorded_at = models.DateTimeField(null=True, default="1920-1-1")

class user_blood_sugar(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    sugar = models.FloatField(null=True, default=0)
    time_period = models.IntegerField(null=True, default=0)
    drug = models.IntegerField(null=True, default=0)
    exercise = models.IntegerField(null=True, default=0)
    recorded_at = models.DateTimeField(null=True, default="1920-1-1")

class user_default(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    sugar_delta_max = models.IntegerField(null=True, default=0)
    sugar_delta_min = models.IntegerField(null=True, default=0)
    sugar_morning_max = models.IntegerField(null=True, default=0)
    sugar_morning_min = models.IntegerField(null=True, default=0)
    sugar_evening_max = models.IntegerField(null=True, default=0)
    sugar_evening_min = models.IntegerField(null=True, default=0)
    sugar_before_max = models.IntegerField(null=True, default=0)
    sugar_before_min = models.IntegerField(null=True, default=0)
    sugar_after_max = models.IntegerField(null=True, default=0)
    sugar_after_min = models.IntegerField(null=True, default=0)
    systolic_max = models.IntegerField(null=True, default=0)
    systolic_min = models.IntegerField(null=True, default=0)
    diastolic_max = models.IntegerField(null=True, default=0)
    diastolic_min = models.IntegerField(null=True, default=0)
    pulse_max = models.IntegerField(null=True, default=0)
    pulse_min = models.IntegerField(null=True, default=0)
    weight_max = models.IntegerField(null=True, default=0)
    weight_min = models.IntegerField(null=True, default=0)
    bmi_max = models.IntegerField(null=True, default=0)
    bmi_min = models.IntegerField(null=True, default=0)
    body_fat_max = models.IntegerField(null=True, default=0)
    body_fat_min = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(null=True, default="1920-1-1")
    updated_at = models.DateTimeField(null=True, default="1920-1-1")

class user_diary(models.Model):	
    user_id = models.IntegerField(null=True, default=0)
    description = models.CharField(max_length=150, null=False, default="")
    meal = models.IntegerField(null=False, default=0)
    tag = models.CharField(max_length=255, null=False, default="")
    image = models.CharField(max_length=500, null=False, default="")
    lat = models.CharField(max_length=5, null=False, default="")
    lng = models.CharField(max_length=5, null=False, default="")
    recorded_at = models.DateTimeField(null=True, default="1920-1-1")

class user_friend(models.Model):
    sender_id = models.IntegerField(null=True, default=0)
    receiver_id = models.IntegerField(null=True, default=0)
    status = models.IntegerField(null=True, default=0)
    read = models.IntegerField(null=False, default=0)
    type = models.IntegerField(null=True, default=0)
    updated_at = models.DateTimeField(null=True, default="1920-1-1")
    created_at = models.DateTimeField(null=True, default="1920-1-1")

class user_share(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    type = models.IntegerField(null=True, default=0)
    row_id = models.IntegerField(null=True, default=0)
    relation_type = models.IntegerField(null=True, default=0)

class user_care(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    member_id = models.IntegerField(null=True, default=1)
    reply_id = models.IntegerField(null=True, default=None)
    message = models.CharField(max_length=255, null=True, default="")
    updated_at = models.DateTimeField(null=True, default="1920-1-1")
    created_at = models.DateTimeField(null=True, default="1920-1-1")

class news(models.Model):
    member_id = models.IntegerField(null=True, default=0)
    group = models.IntegerField(null=True, default=0)
    message = models.CharField(max_length=255, null=True, default="")
    pushed_at = models.DateTimeField(null=True, default="1920-1-1")
    created_at = models.DateTimeField(null=True, default="1920-1-1")
    updated_at = models.DateTimeField(null=True, default="1920-1-1")

class user_medical(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    diabetes_type = models.IntegerField(null=True, default=0)
    oad = models.IntegerField(null=True,default=0)
    insulin = models.IntegerField(null=True,default=0)
    anti_hypertensives = models.IntegerField(null=True,default=0)
    created_at = models.DateTimeField(null=True, default="1920-1-1")
    updated_at = models.DateTimeField(null=True, default="1920-1-1")

class user_a1c(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    a1c = models.IntegerField(null=True, default=0)
    recorded_at = models.DateTimeField(null=True, default="1920-1-1")
    created_at = models.DateTimeField(null=True, default="1920-1-1")
    updated_at = models.DateTimeField(null=True, default="1920-1-1")

class user_settings(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    after_recording = models.BooleanField(null=False, default=False)
    no_recording_for_a_day = models.BooleanField(null=False, default=False)
    over_max_or_under_min = models.BooleanField(null=False, default=False)
    after_meal = models.BooleanField(null=False, default=False)
    unit_of_sugar = models.BooleanField(null=False, default=False)
    unit_of_weight = models.BooleanField(null=False, default=False)
    unit_of_height = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(null=True, default="1920-1-1")
    updated_at = models.DateTimeField(null=True, default="1920-1-1")

class user_drugs(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    type = models.IntegerField(null=False, default=0)
    name = models.CharField(max_length=50, null=True, default="")
    recorded_at = models.DateTimeField(null=True, default="1920-1-1")
    updated_at = models.DateTimeField(null=True, default="1920-1-1")
    created_at = models.DateTimeField(null=True, default="1920-1-1")

class user_vip(models.Model):
    user_id = models.IntegerField(null=True, default=0)
    level = models.IntegerField(null=True, default=0)
    remark = models.FloatField(null=True, default=0)
    started_at = models.DateTimeField(null=True, default="1920-1-1")
    ended_at = models.DateTimeField(null=True, default="1920-1-1")
    created_at = models.DateTimeField(null=True, default="1920-1-1")
    updated_at = models.DateTimeField(null=True, default="1920-1-1")
