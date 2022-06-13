from django.contrib import admin
from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import PreferredProducts as PreferredProductsModel
from django.contrib.auth.models import Group


# unregister group model
admin.site.unregister(Group)
# register User Model in user app
admin.site.register(UserModel)
# register UserProfile Model in user app
admin.site.register(UserProfileModel)

class PreferredProductsAdmin(admin.ModelAdmin):
    # admin 선호상품 페이지에서 id와 name이 같이 보여지도록 함
    # list_display: ('id',) : 여기에 ,가 있고 없고가 중요!
    # 리스트 또는 튜플만 올 수 있음!
    # 리스트로 하거나, 쉼표를 사용하거나
    # list_display = ('id') X
    # list_display = ('id',) O
    # list_display = ['id'] O
    list_display = ['id', 'name']
    # list_display_links = ['name'] # list_display로 지정된 이름중에, detail 링크를 걸 속성 리스트
    # list_filter = ['is_publish'] # 지정 필드값으로 필터링 옵션 제공
    # search_fields = ['name'] # admin내 검색 UI를 통해, DB를 통한 where 쿼리 대상 필드리스트
    
    # def short_desc(self, item):
        # return item.desc[:20]

# PreferredProductsModel 모델에 위에서 정의한 PreferredProductsAdmin 설정을 가져다 쓸 것임
admin.site.register(PreferredProductsModel, PreferredProductsAdmin)
