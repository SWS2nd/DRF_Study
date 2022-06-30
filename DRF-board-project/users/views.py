from django.contrib.auth.models import User as UserModel
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from users import serializers
from .models import Profile as ProfileModel


# Django Rest Framework에서는 GenericAPIView에 List, Create 등 다양한 믹스인(Mixin) 클래스를 결합해 APIView를 구현할 수 있음.
# GenericAPIView는 CRUD(생성/읽기/수정/삭제)에서 공통적으로 사용되는 속성을 제공하고, Mixin은 CRUD 중 특정 기능을 수행하는 메소드를 제공함.
# GenericAPIView와 Mixins으로 정확한 기능 구현이 어려울 때, Override해서 customizing 할 수 있음.
# Mixin 을 상속함으로서 반복되는 내용을 많이 줄일 수 있었으나, 여러 개를 상속해야 하다보니 가독성이 떨어짐. 
# 그리하여 rest_framework 에서는 저들을 상속한 새로운 클래스를 정의해 놓음.
# 총 9개의 클래스
# generics.CreateAPIView : 생성(post 메소드 핸들러 제공)
# generics.ListAPIView : 목록(get 메소드 핸들러 제공)
# generics.RetrieveAPIView : 조회(get 메소드 핸들러 제공)
# generics.DestroyAPIView : 삭제(delete 메소드 핸들러 제공)
# generics.UpdateAPIView : 수정(put, patch 메소드 핸들러 제공)
# generics.RetrieveUpdateAPIView : 조회/수정(get, put, patch 메소드 핸들러 제공)
# generics.RetrieveDestroyAPIView : 조회/삭제(get, delete 메소드 핸들러 제공)
# generics.ListCreateAPIView : 목록/생성(get, post 메소드 핸들러 제공)
# generics.RetrieveUpdateDestroyAPIView : 조회/수정/삭제(get, put, patch, delete 메소드 핸들러 제공)
# 회원가입 뷰
class RegisterView(generics.CreateAPIView): # generics.CreateAPIView : 생성(post 메소드 핸들러 제공)
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer


# 로그인 요청은 1차적인 보안을 위해 POST 요청으로 처리할 것이며, 시리얼라이저를 통과하여 얻어온 토큰을 응답해 주는 방식으로 구현
# 로그인 뷰
class LoginView(generics.GenericAPIView): # 모델에 영향을 주지 않기 때문에 특별한 제너릭을 사용하지 않고 기본 GenericAPIView를 사용
    serializer_class = LoginSerializer
    
    def post(self, request):
        # serializer = serializer클래스(여러가지 인자)
        serializer = self.get_serializer(data=request.data) # 유효성 검사에서 사용될 인스턴스를 serialize해서 반환. 해당 인자를 serialize해 주는 메소드
        # 일반적인 serializer의 유효성 검사는
        # if not serializer.is_valid():
        #       raise ValidationError(serializer.errors) # is_valid() False 시, restapi는 이 예외를 포착하고 list 또는 dict의 형태로 제공된 오류와 함께 400 응답을 반환
        # 에러 발생시 serializer.errors로 list 또는 dict 형태의 에러 메시지 호출 가능
        # 위와 같은 방식으로 진행되는데 이를 좀 더 깔끔하게 한 줄로 표현하면 아래와 같이 표현할 수 있음
        serializer.is_valid(raise_exception=True) # 데이터를 역직렬화할 때 검증된 데이터에 액세스하거나 객체 인스턴스를 저장하기 전에 항상 is_valid()를 호출해야 함.
        # 위 is_valid()에서 True 시,
        token = serializer.validated_data # validate()의 리턴값인 Token을 받아옴.
        # print(type(serializer.validated_data)) 해당 데이터 타입은 <class 'rest_framework.authtoken.models.Token'>
        
        # cf. DRF - Serializer 데이터 접근3가지
        # 1. serializer.initial_data : 유효성 검사를 하기 전에 필드에 접근할 수 있다.
        # 2. serializer.validated_data : 유효성 검사를 통과한 필드에 접근을 할 수 있다.
        # 3. serializer.data : 유효성 검사를 통과하고 save된 필드에 접근할 수 있다.
        
        return Response({'token': token.key}, status=status.HTTP_200_OK)


# 프로필에서 만들어야 될 기능은 조회 및 수정 기능
# 프로필 뷰
class ProfileView(generics.RetrieveUpdateAPIView): # generics.RetrieveUpdateAPIView : 조회/수정(get, put, patch 메소드 핸들러 제공)
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    