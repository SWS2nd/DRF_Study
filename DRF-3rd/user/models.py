from enum import unique
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField


# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField("이메일 주소", max_length=100)
    password = models.CharField("비밀번호", max_length=256)
    fullname = models.CharField("이름", max_length=20)
    join_date = models.DateTimeField("가입일", auto_now_add=True)

	# is_active가 False일 경우 계정이 비활성화됨(일반적으로 계정 삭제를 할 경우, 완전한 삭제 보다 비활성화를 하는 경우가 많음)
    is_active = models.BooleanField(default=True)

    # is_staff에서 해당 값 사용
    is_admin = models.BooleanField(default=False)
    
    # id로 사용 할 필드 지정.(이메일 등 다른 필드도 id로 사용할 수 있음)
    # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.
    USERNAME_FIELD = 'username'

    # user를 생성할 때 입력받은 필드 지정(superuser 포함)
    # serializer를 쓰면 아래 필드는 잘 사용하지 않게 된다.
    REQUIRED_FIELDS = []
    
    objects = UserManager() # custom user 생성 시 필요
    
    def __str__(self):
        return f"{self.username} / {self.email}"

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True
    
    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label): 
        return True
    
    # admin 권한 설정
    # 성이 '이'씨인 사람만 admin 페이지에 접근하도록 할 수도 있음
    @property
    def is_staff(self): 
        return self.is_admin

class UserProfile(models.Model):
    # verbose_name 옵션 : Django 모델을 admin 페이지에서 조회할 때, 필드명 대신 알아보기 쉬운 단어로 지정하는 것
    user = models.OneToOneField(to=User, verbose_name="사용자", primary_key=True, on_delete=models.CASCADE)
    
    # through 옵션으로 중간 테이블을 아래쪽에 직접 만든것을 사용하겠다고 명시(뺄 경우, 자동 생성되는 중간 테이블 사용)
    # through='UserProfilePreferredProducts'
    preferred_products = models.ManyToManyField(to="PreferredProducts", verbose_name="선호상품")
    
    # Add 전화번호
    # 외부 라이브러리인 phonenumber_field 패키지를 설치 후 사용하였습니다.
    # PhoneNumberField필드는 내부적으로 CharField공간을 기반으로하며 국제 전화 번호 표준에 따라 문자열 형태로 숫자를 저장합니다.
    phone_number = PhoneNumberField("전화번호", unique=True, null=True, default='')
    
    # Add 성별
    GENDER_CHOICES =(
        ('M','남성(Man)'),
        ('W','여성(Woman)'),
    )
    # choices 속성은 해당 필드가 선택되어야하는 경우에 지정해줍니다.
    gender = models.CharField('성별', max_length=20, choices=GENDER_CHOICES, null=True)
    
    # Add 생년월일
    birth_date = models.DateField('생년월일', null=True)
    
    # Add 소개
    introduction = models.TextField("소개")
    
    def __str__(self):
        return f"{self.user.fullname} 님의 프로필 입니다."
    
class PreferredProducts(models.Model):
    name = models.CharField("선호상품", max_length=100)
    
    def __str__(self):
        return self.name

# 중간 테이블을 아래 처럼 직접 생성해서 써도 되고, 아니면 ManyToManyField에서 through 옵션만 빼고 장고에서 자동으로 만들어주는 중간 테이블을 사용해도 된다.
#class UserProfilePreferredProducts(models.Model):
#    user_profile = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
#    prefer_prod = models.ForeignKey(to=PreferredProducts, on_delete=models.CASCADE)
