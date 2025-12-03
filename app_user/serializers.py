from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 在负载中添加额外信息
        token["id"] = user.id
        token["username"] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # 返回额外的用户信息
        data.update(
            {
                "id": self.user.id,
                "username": self.user.username,
            }
        )
        return data
