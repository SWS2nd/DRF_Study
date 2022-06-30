from rest_framework import permissions


class CustomReadOnly(permissions.BasePermission):
    # GET : 누구나 가능 / PUT, PATCH : 로그인 한 해당 유저
    def has_object_permission(self, request, view, obj): # 프로필 전체 권한이 아닌 각 프로필 객체의 권한을 건드리므로 has_object_permission() 메소드를 활용
        # permissions.SAFE_METHODS : SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        # 요청으로 들어온 메소드가 GET과 같은 데이터에 영향을 미치지 않는 메소드이면 True를 반환하여 통과시키며,
        if request.method in permissions.SAFE_METHODS:
            return True
        # PUT, PATCH와 같은 데이터에 영향을 미치는 메소드는 요청으로 들어온 유저와 객체의 유저를 비교하여 같은 경우 통과시킴.
        # 즉 토큰이 유효한 토큰이더라도 해당 토큰의 유저가 해당 프로필의 유저와 같지 않다면, 통과하지 않음.(다른 유저가 프로필을 수정하는 것을 사전에 방지 가능)
        return obj.user == request.user
    