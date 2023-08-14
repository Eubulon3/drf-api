from django.urls import path, include
from apiapp import views
from rest_framework.routers import DefaultRouter

app_name = "apiapp"

router = DefaultRouter()
router.register("profile", views.ProfileViewSet)
router.register("approval", views.FriendRequestViewSet)
router.register("schedule", views.ScheduleViewSet)
router.register("memberApproval", views.MemberRequestViewSet)
router.register("contribution", views.ContributionViewSet)
router.register("notice", views.NoticeViewSet)
router.register("payment", views.PaymentViewSet)
router.register("addItem", views.AddItemViewSet)
router.register("managemoney", views.ManageMoneyViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.CreateUserView.as_view(), name = "register"),
    path("myprofile/", views.MyProfileListView.as_view(), name = "myprofile"),
    path("myfriends/", views.MyFriendsListView.as_view(), name = "myfrien ds"),
    path("searchuser/", views.SearchUser.as_view(), name = "serchuser"),
    path("myschedule/", views.MyScheduleListView.as_view(), name = "myschedule"),
    path("mypayment/", views.MyPaymentListView.as_view(), name = "mypayment"),
    path("searchsche/", views.SearchSchedule.as_view(), name = "searchsche"),
    # path("scheduledetail/", views.ScheduleListView.as_view(), name = "scheduledetail"),
]
