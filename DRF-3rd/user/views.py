from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework import status
from django.contrib.auth import get_user_model

from user.models import User as UserModel


# 헬로우 월드~
class HelloWorld(APIView):
    def get(self, request, *args, **kwargs):
        return Response({'msg': 'Hello World!!!'})
    
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

# 연습용
class HttpMethodsPractice(APIView):
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


# 로그인
class Login(APIView):
    def get(self, request):
        user = request.user.is_authenticated
        if user:
            return redirect('blog:home')
        else:
            return render(request, 'user/login.html')
    
    def post(self, request):
        # 뒤쪽의 None은 POST로 넘겨받은 데이터 중에 'username'이 없다면
        # None으로 처리하겠다는 의미.
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        # authenticate(request=None, **credentials) : User 인증 함수. 자격 증명이 유효한 경우 User 객체를, 그렇지 않은 경우 None을 반환
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login(request, user, backend=None) : 로그인 함수. Django의 세션 프레임워크를 사용하여 세션에 인증된 사용자의 ID를 저장
            login(request, user)
            return redirect('blog:home')
        else:
            # messages framework : 쿠키 및 세션 기반의 1회성 메시지를 담는 용도(메시지를 하나의 HttpRequest 인스턴스에 임시로 저장하고 바로 다음 request에 표시됨)
            messages.error(request, '존재하지 않는 계정이거나 패스워드가 일치하지 않습니다.')
            return redirect('user:login')

# 로그아웃
class Logout(APIView):
    def get(self, request):
        # 현재 로그인된 세션에 대한 모든 데이터를 삭제
        logout(request)
        return redirect('user:login')
    
# 회원가입
class SignUp(APIView):
    def get(self, request):
        user = request.user.is_authenticated
        if user:
            return redirect('blog:home')
        else:
            return render(request, 'user/signup.html')
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        password2 = request.data.get('password2', '')
        email = request.data.get('email', '')
        fullname = request.data.get('fullname', '')
        # 아래 필드들은 따로 다루는 것으로.
        preferred_products = request.data.get('preferred_products', '')
        phone_number = request.data.get('phone_number', '')
        gender = request.data.get('gender', '')
        birth_date = request.data.get('birth_date', '')
        introduction = request.data.get('introduction', '')
        
        # 회원가입시 비밀번호가 같아야 되는 부분을 작성.
        # 비밀번호와 비밀번호 확인이 같지 않다면,
        # GET에서 작성한 signup.html을 다시 보여줄 것이다.
        if password != password2:
            # 패스워드가 같지 않다고 알림
            return render(request, 'user/signup.html', {'error':'패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밀번호는 필수 입력 값 입니다!'})
            else:
                # 사용자가 DB 안에 있는지 검사하는 함수인 get_user_model()을 사용하여 필터링.
                exist_user = get_user_model().objects.filter(username=username)
                # 회원가입시 my_user db에 동일한 username이 있다면 가입되지 않도록 한다.
                if exist_user:
                    return render(request, 'user/signup.html', {'error': '사용자가 이미 존재합니다.'})
                else:
                    # create_user() 함수는 상속받은 BaseUserManager 클래스에서 제공해주는 함수.(생성 및 저장 후 user를 return함.)
                    UserModel.objects.create_user(username=username, password=password, email=email, fullname=fullname)
                    return redirect('user:login')

# 사용자 정보
class UserInformation(APIView):
    def get(self, request):
        # 로그인 한 사용자
        logged_in_user = request.user
        return render(request, 'user/user_inform.html', {'user_name': logged_in_user.username, 'user_email': logged_in_user.email})
    def post(self, request):
        pass
    