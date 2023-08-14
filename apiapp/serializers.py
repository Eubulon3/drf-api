from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Schedule, FriendRequest, MemberRequest, Notice, Payment, Contribution, AddItem, Manage
from django.db.models import Q

#基本的にはモデルごとに定義
class UserSerializers(serializers.ModelSerializer):

    class Meta:
        #現在is_activeなユーザーモデルを取得
        model = get_user_model()
        #serializerで取り扱いたいパラーメータ
        fields = ("id", "email", "password")
        #clientからは取得できない(getメソッド)
        extra_kwargs = {"password": {"write_only": True}}
    
    #balidated_data: validation後のデータ(辞書型)
    def create(self, validated_data):

        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializers(serializers.ModelSerializer):

    #シンプルな表記に変更
    created_on = serializers.DateTimeField(format = "%Y-%m-%d", read_only = True)

    class Meta:
        model = Profile
        fields = ("id", "nickName", "userProfile", "created_on", "img")
        extra_kwargs = {
            "userProfile": {"read_only": True}
        }


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ('id','askFrom','askTo','approved')
        extra_kwargs = {'askFrom': {'read_only': True}}

class MemberRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberRequest
        fields = ("id", "askFrom", "askTo", "approved")

class ScheduleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ("id", "title", "started_at", "finished_at", "budget", "scheduled_by", "password")
        extra_kwargs = {
            "scheduled_by": {"read_only": True}
        }

# ↓スケジュールリストを全て取得してメンバー情報を追加取得
# class ScheduleDetailSerializers(serializers.ModelSerializer):

#     # SerializerMethodField は get_xxxx ってなっているメソッドをコールする
#     member = serializers.SerializerMethodField()

#     class Meta:
#         model = Schedule
#         fields = ("id", "title", "started_at", "finished_at", "budget", "scheduled_by", "password", "member")
#         extra_kwargs = {
#             "scheduled_by": {"read_only": True}
#         }

#     #おそらくobjはmodelインスタンス
#     def get_member(self, obj):
#         try:
#             return MemberRequestSerializer(MemberRequest.objects.all().filter(Q(askFrom = Schedule.objects.get(id = obj.id)) & Q(askTo = self.context["request"].user)), many=True).data
#         except:
#             return None
    

# ↓自分の参加するリクエストのみを表示し、そのスケジュールのdetail取得
class MyScheduleSerializers(serializers.ModelSerializer):

    # SerializerMethodField は get_xxxx ってなっているメソッドをコールする
    details = serializers.SerializerMethodField()

    class Meta:
        model = MemberRequest
        fields = ("id", "askFrom", "askTo", "approved", "details")

    #おそらくobjはmodelインスタンス
    def get_details(self, obj):
        try:
            return ScheduleSerializers(obj.askFrom).data
        except:
            return None

class ContributionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contribution
        fields = ("id", "item", "point", "contributionSchedule")


class NoticeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = ("id", "read", "state", "userNotice", "created_at")
        extra_kwargs = {
            "userNotice": {"read_only": True},
            "created_at": {"read_only": True},
        }

class PaymentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ("id", "money", "paymentSchedule", "paymentTo", "paymentFrom", "completed", "created_at")
        extra_kwargs = {
            "created_at": {"read_only": True},
        }

class AddItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddItem
        fields = ("id", "item", "contents", "scheduleAdd")

class ManageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manage
        fields = ("id", "scheduleManage", "userManage", "money")
        extra_kwargs = {
            "scheduleManage": {"read_only": True}
        }