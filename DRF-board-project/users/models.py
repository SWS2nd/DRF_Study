from django.db import models
from django.contrib.auth.models import User as UserModel
# Django에는 프레임워크의 다른 곳에서 작업이 발생할 때 분리된 애플리케이션이 알림을 받는 데 도움이 되는 "신호 디스패처(signal dispatcher)"가 포함되어 있음
# 간단히 말해서 신호를 통해 특정 발신자는 일련의 수신자에게 어떤 조치가 발생했음을 알릴 수 있음
# 많은 코드 조각이 동일한 이벤트에 관심이 있을 때 특히 유용함.
from django.db.models.signals import post_save # 모델의 save() 메서드가 호출되기 전(pre_save)이나 후(post_save)에 전송하는 이벤트
from django.dispatch import receiver


# 유저 프로필 모델
class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True) # primary_key를 UserModel의 pk로 설정해서 통합 관리
    nickname = models.CharField(max_length=256) # 닉네임
    position = models.CharField(max_length=256) # 직종
    subjects = models.CharField(max_length=256) # 관심사
    # upload_to 옵션으로 이미지가 업로드 될 경로를 지정해주고, default 옵션으로 이미지를 선택하지 않았을 시 대신 올라갈 기본값을 설정.
    image = models.ImageField(upload_to='profile/', default='default.png') # 프로필 이미지 


# User 모델이 save() 메서드가 호출 된 후 즉, post_save 이벤트를 발생시켰을 때 해당 이벤트가 일어났다는 사실을 받아서, 
# 해당 유저 인스턴스와 연결되는 프로필 데이터를 생성하도록 해주는 데코레이터 및 함수.
@receiver(post_save, sender=UserModel) # 해당 데코레이터를 사용 함으로써 프로필을 생성해 주는 코드를 직접 작성하지 않아도 알아서 유저 생성 이벤트를 감지해 프로필을 자동으로 생성 가능해짐.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
