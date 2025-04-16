from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                tokens = get_tokens_for_user(user)

                return Response({
                    "user": serializer.data,
                    "tokens": tokens
                })

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": "Something went wrong",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response({
                    "msg": "შეიყვანეთ სახელი და პაროლი"
                })


            user = authenticate(username = username, password = password )



            if user is not None:
                tokens = get_tokens_for_user(user)
                return Response({
                    "username": user.username,
                    "email": user.email,
                    "tokens": tokens
                }, status = status.HTTP_200_OK)


            return Response({
                "msg" : "მომხმარებლის სახელი ან პაროლი არასწორია"
            })


        except Exception as e:
            return Response({
                "error": "Something went wrong",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
