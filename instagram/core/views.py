from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.template.defaulttags import comment
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, PostSerializer, CommentSerializer
from .models import Post, User, Comment


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

class MyPostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": "Something went wrong",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        posts = Post.objects.filter(user=request.user).order_by("-created_at")
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class Delete_or_edit_myPost(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request,pk):
        try:
            post = get_object_or_404(Post, pk=pk)
            if post.user != request.user:
                return Response({'msg': 'u cant edit this post'})
            serializer = PostSerializer(post,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "error": "Something went wrong",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class User_Post(APIView):
    def get(self, request,username):
        user = get_object_or_404(User,username=username)
        posts = Post.objects.filter(user=user).order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            post = get_object_or_404(Post, id = request.data.get("post"))
            serializer = CommentSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user = request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST  )
        except Exception as e:
            return Response({
                "error": "Something went wrong",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentListView(APIView):
    def get(self, request, post_id):
        try:
            comment = Comment.objects.filter(post__id = post_id).order_by("-created_at")
            serializer = CommentSerializer(comment, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": "Something went wrong",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)