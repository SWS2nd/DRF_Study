from django.contrib.auth.models import User as UserModel
from rest_framework import generics

from .serializers import RegisterSerializer


# Django Rest Framework에서는 GenericAPIView에 List, Create 등 다양한 믹스인(Mixin) 클래스를 결합해 APIView를 구현할 수 있음.
# GenericAPIView는 CRUD(생성/읽기/수정/삭제)에서 공통적으로 사용되는 속성을 제공하고, Mixin은 CRUD 중 특정 기능을 수행하는 메소드를 제공함.
# GenericAPIView와 Mixins으로 정확한 기능 구현이 어려울 때, Override해서 customizing 할 수 있음.
# Mixin 을 상속함으로서 반복되는 내용을 많이 줄일 수 있었으나, 여러 개를 상속해야 하다보니 가독성이 떨어짐. 
# 그리하여 rest_framework 에서는 저들을 상속한 새로운 클래스를 정의해 놓음.
# 총 9개의 클래스
# generics.CreateAPIView : 생성
# generics.ListAPIView : 목록
# generics.RetrieveAPIView : 조회
# generics.DestroyAPIView : 삭제
# generics.UpdateAPIView : 수정
# generics.RetrieveUpdateAPIView : 조회/수정
# generics.RetrieveDestroyAPIView : 조회/삭제
# generics.ListCreateAPIView : 목록/생성
# generics.RetrieveUpdateDestroyAPIView : 조회/수정/삭제
class RegisterView(generics.CreateAPIView): # generics.CreateAPIView 사용
    queryset = UserModel.objects.all()
    serializer_class = RegisterSerializer
