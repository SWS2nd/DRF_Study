from rest_framework import viewsets

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
    
    # REST 프레임워크에 포함된 기본 라우터는 list/create/retrieve/update/destroy 스타일 작업의 표준 세트에 대한 경로를 제공.
    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve': # 시스템의 현재 action이 list(나열) or retrieve(검색)인 경우, 즉 게시글 나열 또는 검색시,
            return PostSerializer
        return PostCreateSerializer # 게시글을 생성, 수정 등의 경우
    
    # 게시글 생성시 사용자 프로필 및 작성자를 자동으로 생성해주도록 함.
    def perform_create(self, serializer):
        profile = ProfileModel.objects.get(user=self.request.user) # 현재 게시글 생성을 요청한 사용자의 프로필
        serializer.save(author=self.request.user, profile=profile) # 해당 시리얼라이저의 author, profile에 요청한 사용자의 프로필과 요청한 사용자를 작성자로 하여 저장.
