from rest_framework import serializers
from .models import User, Post, Comment, Reply
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', "email", "password", "password2", 'first_name', 'last_name' ]

    def validate(self, attrs):


        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"msg": "პაროლები არ ემთხვევა"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user','id','image','caption','created_at']
        read_only_fields = ['user','id','created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'text', 'created_at']


class ReplySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reply
        fields = ['id', 'user', 'comment', 'text', 'created_at']

