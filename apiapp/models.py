from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


def upload_avatar_path(instance, filename):
    ext = filename.split(".")[-1]
    return "/".join(["avatars", str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])


class UserManager(BaseUserManager):

    #usernameをemailに
    def create_user(self, email, password = None):

        if not email:
            raise ValueError("email is must")

        #userというインスタンス作成, emailの正規化(大文字→小文字)など
        user = self.model(email = self.normalize_email(email))
        #passwordがハッシュ化される
        user.set_password(password)
        #作ったインスタンスをdbにsave
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password = None):

        #userというインスタンス作成(create_userから)
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


#django提供のユーザモデルをオーバーライド
class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique = True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)

    #Userクラスの中にUserManagerというクラスが存在
    objects = UserManager()

    USERNAME_FIELD = "email"

    #タグのようなもの
    def __str__(self):
        return self.email

class Profile(models.Model):
    nickName = models.CharField(max_length=20, unique=True)
    userProfile = models.OneToOneField(settings.AUTH_USER_MODEL, related_name = "userProfile",on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to=upload_avatar_path, blank = True, null = True)

    def __str__(self):
        return self.nickName
    
class FriendRequest(models.Model):
    askFrom = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="askFrom", on_delete=models.CASCADE)
    askTo = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="askTo", on_delete=models.CASCADE)
    approved = models.BooleanField(default = False)

    class Meta:
        unique_together = (("askFrom", "askTo"),)
    
    def __str__(self):
        return str(self.askFrom) + "--->" + str(self.askTo)


class Schedule(models.Model):
    title = models.CharField("タイトル", max_length=30)
    budget = models.IntegerField("予算")
    started_at = models.DateField("開始日", auto_now=False, auto_now_add=False)
    finished_at = models.DateField("終了日", auto_now=False, auto_now_add=False)
    scheduled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="scheduled_by")
    password = models.IntegerField("部屋番号")

    def __str__(self):
        return self.title

class AddItem(models.Model):
    item = models.CharField("追加項目", max_length=10)
    contents = models.TextField("内容", max_length=30)
    scheduleAdd = models.ForeignKey(Schedule, related_name="schedule_add", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.scheduleAdd) + ": " + str(self.item)
    
class MemberRequest(models.Model):
    askFrom = models.ForeignKey(Schedule, related_name="member_askFrom", on_delete=models.CASCADE)
    askTo = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="member_askTo", on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.askFrom) + ": " + str(self.askTo)

class Contribution(models.Model):
    item = models.CharField("貢献項目", max_length=30)
    point = models.IntegerField("pt")
    contributionSchedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Notice(models.Model):
    read = models.BooleanField("既読")
    state = models.IntegerField("state")
    userNotice = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "userNotice", on_delete=models.CASCADE)
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    def __str__(self):
        return self.state

class Payment(models.Model):
    money = models.IntegerField("金額")
    paymentSchedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, blank=True, null = True)
    #支払い
    paymentTo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "PayTo")
    #受け取り
    paymentFrom = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "PayFrom")
    completed = models.BooleanField("達成")
    created_at = models.DateTimeField("作成日時", auto_now_add=True)

    def __str__(self):
        return str(self.paymentFrom) + "--" + str(self.money) + "-->" + str(self.paymentTo)


class Manage(models.Model):
    scheduleManage = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="scheduleManage")
    userManage = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userManage")
    money = models.IntegerField("金額")

    def __str__(self):
        return str(self.userManager) + ":" + str(self.money)
    
