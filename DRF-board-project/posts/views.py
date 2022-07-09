# view 마다 필터 설정할 때 사용(settings.py에 이미 등록해서 상관 없음)
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets

# 좋아요 기능 추가(간단하기에 함수형 뷰로 작성하기 위한 라이브러리들 import)
# GET 요청을 받는 함수형 뷰라는 설정과 로그인 권한이 필요하다는 설정을 위함.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# 만약 객체가 존재하지 않을 때 get()을 이용하여 Http404 예외를 발생시킴.
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from users.models import Profile as ProfileModel
from .models import Post as PostModel
from .permissions import CustomReadOnly
from .serializers import PostSerializer, PostCreateSerializer


# view 대신 viewsets 사용.
# ViewSets 및 라우터는 표준 동작 및 표준 URL을 목표로 하는 경우 API 구현 속도를 높이는 간단한 도구
# ViewSet을 사용하면 개체 목록과 한 개체의 세부 정보를 얻기 위해 별도의 views를 만들 필요가 없음. ViewSet은 목록과 세부 정보를 일관된 방식으로 처리함.
# viewsets을 사용하면 router도 따라옴.
# 라우터를 사용하면 ViewSet을 URL의 "표준화"(전 세계적으로 표준이 아니며 Django REST 프레임워크 작성자가 구현한 일부 구조) 구조에 연결.
# 그렇게 하면 url 패턴을 손으로 만들 필요가 없으며 모든 URL이 일관성이 있음을 보장할 수 있음.
# 많은 urlpattern과 view가 있는 거대한 API를 구현할 때 ViewSet과 Router를 사용하면 큰 차이를 만들 수 있음.
class PostViewSet(viewsets.ModelViewSet):
    queryset = PostModel.objects.all()
    permission_classes = [CustomReadOnly]
    filter_backends = [DjangoFilterBackend] # 필터링 설정
    filterset_fields = ['author', 'likes', 'category'] # 필터링 필드 설정
    
    # REST 프레임워크에 포함된 기본 라우터는 list/create/retrieve/update/destroy 스타일 작업의 표준 세트에 대한 경로를 제공.
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve': # 시스템의 현재 action이 list(나열) or retrieve(검색)인 경우, 즉 게시글 나열 또는 검색시,
            return PostSerializer
        return PostCreateSerializer # 게시글을 생성, 수정 등의 경우
    
    # 게시글 생성시 사용자 프로필 및 작성자를 자동으로 생성해주도록 함.
    def perform_create(self, serializer):
        profile = ProfileModel.objects.get(user=self.request.user) # 현재 게시글 생성을 요청한 사용자의 프로필
        serializer.save(author=self.request.user, profile=profile) # 해당 시리얼라이저의 author, profile에 요청한 사용자의 프로필과 요청한 사용자를 작성자로 하여 저장.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(PostModel, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    return Response({'status': 'ok'})
    