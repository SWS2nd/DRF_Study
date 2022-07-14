from xml.etree.ElementTree import Comment
from rest_framework import serializers

from users.serializers import ProfileSerializer
from .models import Post as PostModel
from .models import Comment as CommentModel


# 댓글을 가져올 때 사용할 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = CommentModel
        fields = ('pk', 'profile', 'post', 'text')
        

# 댓글을 작성할 때 사용할 시리얼라이저
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ('post', 'text')
        

# 게시글에 대한 모든 정보를 Json으로 변환하여 전달해야 하는 시리얼라이저
# 게시글을 가져올 때 사용할 시리얼라이저
class PostSerializer(serializers.ModelSerializer):
    # nested serializer(중첩된 시리얼라이저, 시리얼라이저 안에 또다른 시리얼라이저가 포함된 변수를 만듦 이중으로 연결된 구조.)
    # 이를 작성하지 않는다면 profile 필드에는 profile의 pk 값만 나타나게 됨. 해당 글 작성자의 실제 프로필 정보를 알고 싶기 때문에 중첩으로 작성.
    profile = ProfileSerializer(read_only=True)
    # 위에서 작성한 댓글을 가져올 때 사용할 시리얼라이저를 포함하여 게시글에서 댓글을 불러오도록 함, many=True를 통해 다수의 댓글 포함
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = PostModel
        fields = ('pk', 'profile', 'title', 'category', 'body', 'image', 'published_date', 'likes', 'comments')
        

# 사용자가 게시글 작성시 필요한 시리얼라이저(필요한 필드는 타이틀, 카테고리, 본문, 이미지)
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ('title', 'category', 'body', 'image')
