from rest_framework import permissions


# 커스텀 권한 설정.
# 조회는 누구나 가능 / 글 생성은 로그인 인증된 유저만 가능 / 수정 및 삭제는 로그인 인증된 유저중에서 해당 글을 작성한 유저만 가능.
class CustomReadOnly(permissions.BasePermission):
    # 전체 객체에 대한 권한 설정
    def has_permission(self, request, view):
        if request.method == 'GET': # 조회는 누구나 가능 하도록 설정
            return True
        return request.user.is_authenticated # GET method 이외의 method는 인증된 사용자만(글 생성은 인증된 사용자만) 가능하도록 설정
    
    # 각 객체별 권한 설정(특정 object에 접근하는 순간의 권한 설정)
    def has_object_permission(self, request, view, obj):
        # permissions.SAFE_METHODS : SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        # 요청으로 들어온 메소드가 GET과 같은 데이터에 영향을 미치지 않는 메소드이면 True를 반환하여 통과시키며,
        if request.method in permissions.SAFE_METHODS: 
            return True
        # PUT, PATCH, DELETE와 같은 데이터에 영향을 미치는 메소드는 요청으로 들어온 유저와 객체의 유저를 비교하여 같은 경우 통과시킴.
        # 즉 로그인 한 토큰이 유효한 토큰이더라도 해당 토큰의 유저가 해당 프로필의 유저와 같지 않다면, 통과하지 않음.(다른 유저가 프로필을 수정하는 것을 사전에 방지 가능)
        return obj.author == request.user
    