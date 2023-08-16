from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Schedule,AddItem, Notice, Payment, Contribution, FriendRequest, MemberRequest, Manage
from django.conf import settings
from django.views import View
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


#serializer_classにserializerを割り当てる、
class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializers
    permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProfileSerializers
    queryset = Profile.objects.all()

    #crudのcreateの処理の時
    def perform_create(self, serializer):
        serializer.save(userProfile = self.request.user)


class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    #GET時のqueryset
    def get_queryset(self):
        return self.queryset.filter(Q(askTo=self.request.user) | Q(askFrom=self.request.user))
    
        #crudのc
    def perform_create(self, serializer):
        try:
            serializer.save(askFrom = self.request.user)
        except:
            #同じリクエスト送信回避
            raise ValidationError("User can have only unique request")
    
    def destroy(self, request, *args, **kwargs):
        response = {"message": "Delete is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        response = {"message": "Patch is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class MyProfileListView(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializers
    queryset = Profile.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(userProfile = self.request.user)


class MyFriendsListView(generics.ListAPIView):
    serializer_class = serializers.FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def get_queryset(self):
        try:
            return self.queryset.filter(Q(askTo=self.request.user) | Q(askFrom=self.request.user) & Q(approved=True))
        except:
            return []

class FriendRequestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def get_queryset(self):
        return self.queryset.filter(Q(askTo=self.request.user) | Q(askFrom=self.request.user))
    
    def perform_create(self, serializer):
        try:
            serializer.save(askFrom = self.request.user)
        except:
            #askFrom=askToの際にエラー
            raise ValidationError("User can have only unique request")
    
    def destroy(self, request, *args, **kwargs):
        response = {"message": "Delete is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        response = {"message": "Patch is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class SearchUser(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializers
    queryset = Profile.objects.all()

    def get_queryset(self):

        #GETリクエスト内にname属性=serachが存在していた場合の処理を定義
        if "search" in self.request.GET:
            queryset = Profile.objects.all()
            #検索文字列
            query = self.request.query_params.get("search")
            if query is not None:
                queryset = queryset.filter(nickName__istartswith = query)
            return queryset


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ScheduleSerializers
    queryset = Schedule.objects.all()

    def perform_create(self, serializer):
        serializer.save(scheduled_by = self.request.user)

class MemberRequestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MemberRequestSerializer
    queryset = MemberRequest.objects.all()

    #GET時のqueryset
    def get_queryset(self):
        return self.queryset.filter(askTo=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        response = {"message": "Delete is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        response = {"message": "Patch is not allowed !"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

# class ScheduleListView(generics.ListAPIView):
#     queryset = Schedule.objects.all()
#     serializer_class = serializers.ScheduleDetailSerializers

#自分の参加しているスケジュール全てのリスト(JSON)
class MyScheduleListView(generics.ListAPIView):
    queryset = MemberRequest.objects.all()
    serializer_class = serializers.MyScheduleSerializers

    def get_queryset(self):
        return self.queryset.filter(askTo=self.request.user)


class ContributionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContributionSerializer
    queryset = Contribution.objects.all()


class NoticeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NoticeSerializers
    queryset = Notice.objects.all()

    def perform_create(self, serializer):
        serializer.save(userNotice = self.request.user)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PaymentSerializers
    queryset = Payment.objects.all()


class AddItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AddItemSerializer
    queryset = AddItem.objects.all()

class MyPaymentListView(generics.ListAPIView):
    serializer_class = serializers.PaymentSerializers
    queryset = Payment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(Q(paymentTo = self.request.user) | Q(paymentFrom = self.request.user))


class SearchSchedule(generics.ListAPIView):
    serializer_class = serializers.ScheduleSerializers
    queryset = Schedule.objects.all()

    def get_queryset(self):

        #GETリクエスト内にname属性=serachが存在していた場合の処理を定義(完全一致)
        if "search" in self.request.GET:
            #検索文字列
            query = self.request.query_params.get("search")
            if query is not None:
                queryset = self.queryset.filter(password__exact = query)
            return queryset

class ManageMoneyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ManageSerializer
    queryset = Manage.objects.all()

    def perform_create(self, serializer):
        if "target" in self.request.GET:
            query = self.request.query_params.get("target")
            if query is not None:
                serializer.save(target = query)

class UserListView(generics.ListAPIView):
    User = get_user_model()
    serializer_class = serializers.UserSerializers
    queryset = User.objects.all()

class HostScheduleListView(generics.ListAPIView):
    serializer_class = serializers.ScheduleSerializers
    queryset = Schedule.objects.all()

    def query_set(self):
        return self.queryset.filter(scheduled_by = self.request.user)

