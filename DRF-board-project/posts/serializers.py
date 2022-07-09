from rest_framework import serializers

from users.serializers import ProfileSerializer
from .models import Post as PostModel


# 게시글에 대한 모든 정보를 Json으로 변환하여 전달해야 하는 시리얼라이저
# 게시글을 GET으로 볼 때 해당 시리얼라이저의 필드들을 보여줌.
class PostSerializer(serializers.ModelSerializer):
    # nested serializer(중첩된 시리얼라이저, 시리얼라이저 안에 또다른 시리얼라이저가 포함된 변수를 만듦 이중으로 연결된 구조.)
    profile = ProfileSerializer(read_only=True) # 이를 작성하지 않는다면 profile 필드에는 profile의 pk 값만 나타나게 됨. 해당 글 작성자의 실제 프로필 정보를 알고 싶기 때문에 중첩으로 작성.
    
    class Meta:
        model = PostModel
        fields = ('pk', 'profile', 'title', 'category', 'body', 'image', 'published_date', 'likes')
        

# 사용자가 게시글 작성시 필요한 시리얼라이저(필요한 필드는 타이틀, 카테고리, 본문, 이미지)
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ('title', 'category', 'body', 'image')
