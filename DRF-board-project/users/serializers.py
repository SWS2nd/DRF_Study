# Serializer
# 요청으로 들어온 데이터를 Django 데이터로 변환하여 저장하는 기능을 수행.
# 객체를 자바스크립트 및 프런트 엔드 프레임워크에서 이해할 수 있는 데이터 유형으로 변환하는 역할.
# 위 외에도 Validation 즉, 검증 기능도 존재함.

from django.contrib.auth.models import User as UserModel
from django.contrib.auth.password_validation import validate_password # django의 기본 패스워드 검증 도구
from rest_framework import serializers
from rest_framework.authtoken.models import Token as TokenModel
from rest_framework.validators import UniqueValidator # 이메일 중복 방지 시 검증 도구


# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    # 시리얼라이저의 필드들 : serializer 필드는 primitive value와 internal datatypes간의 변환을 핸들링. 또한 input value에 대한 validating도 해줌.
    # 각각의 serializer field class는 적어도 3개의 args를 받음. 몇몇 Field는 추가적인 (field-specific) args가 필요
    email = serializers.EmailField(
        required=True, # required : default=True, deserialization 할 때 포함되어있지 않으면 에러 반환. 
                        #           deserialization시 필수가 아니면 False로 해놓으면 인스턴스를 serializng attribute나 dict key를 누락시킴 => outut에서 포함되지 않음
        validators=[UniqueValidator(queryset=UserModel.objects.all())], # 이메일 중복 검증
    )
    password = serializers.CharField(
        write_only=True, # write_only : default=False, True로 되어있으면 인스턴스를 updating, creating 할 때에는 사용되지만 serializing 할때는 포함되지 않음
        required=True,
        validators=[validate_password], # 비밀번호 검증
    )
    password2 = serializers.CharField(write_only=True, required=True) # 비밀번호 확인
    
    class Meta:
        model = UserModel
        fields = ('username', 'password', 'password2', 'email')
    
    # 시리얼라이저의 validate 메소드 활용
    def validate(self, data): # 추가적인 비밀빈호 일치 여부 확인
        # 비밀번호가 다를 경우 serializers의 ValidationError를 발생시킴
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': '비밀번호가 일치하지 않습니다.'}
            )
        return data

    # 시리얼라이저의 create 메소드 활용
    # CREATE 요청에 대해 create 메소드를 오버라이딩하여 유저를 생성하고 토큰을 생성하게 함.
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        token = TokenModel.objects.create(user=user)
        return user
