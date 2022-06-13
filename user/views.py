from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class HelloWorld(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"msg": "Hello World!!!"})
    
# 만약 권한을 직접 custom해서 사용하고 싶을 경우,
# 아래 처럼 대략적으로 권한과 관련된 IsAuthenticated 클래스 등을 복붙해서 아래처럼 커스텀 해보면 된다.
class MyCustomPermission(permissions.BasePermission):

    # 해당 permission을 보면, request한 user가 있고, 로그인 되었으면 둘 다 True이면 view를 실행하도록 되어있다.
    # 이를 필요에 맞게 custom해서 사용하면 되겠다.
    # def has_permission(self, request, view):
    #     return bool(request.user and request.user.is_authenticated)

    def has_permission(self, request, view):
        user = request.user
        # 요청한 user 존재, 로그인된 user, user의 permission_rank가 5 초과인 경우 통과되도록 권한 custom 
        result = bool(user and user.is_authenticated and user.permission_rank > 5)
        return result

class UserApiView(APIView):
    # permission_classes
    # 이 퍼미션 클래스를 지정하지 않으면 기본으로 지정된 것으로 됩니다.라고 permission_classes에 아래와 같이 작성되어있음.
    # permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    
    # permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능
    # permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    
    # 위에서 custom한 permission 클래스를 사용하고 싶을 때
    # permission_classes = [MyCustomPermission]
    
    # 우선은 누구나 조회 가능하도록 하겠음
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({'message': 'get success!!'})

    def post(self, request):
        return Response({'message': 'post success!!'})

    def put(self, request):
        return Response({'message': 'put success!!'})

    def delete(self, request):
        return Response({'message': 'delete success!!'})