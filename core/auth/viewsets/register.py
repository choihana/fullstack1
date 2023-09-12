from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from core.auth.serializers import RegisterSerializer


class RegisterViewSet(ViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    #실제로 회원가입을 처리
    def create(self,request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #유효성 검사 통과하면 사용자를 생성하고, 해당 사용자에 대한 JWT refresh 토근을 생성함
        refresh = RefreshToken.for_user(user)
        res = {
            'refresh' : str(refresh),
            'access': str(refresh.access_token),
        }

        return Response({
            'user':serializer.data,
            'refresh':res['refresh'],
            'token': res['access']
        }, status = status.HTTP_201_CREATED)



