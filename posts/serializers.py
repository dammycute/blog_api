from rest_framework import serializers
from .models import Post, Tag

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True}
        }

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError(
    #             {"password": "Password fields didn't match."}
    #         )
    #     return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PostSerializers(serializers.ModelSerializer):
    readtime = serializers.SerializerMethodField(source = 'get_read_time')
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'tag', 'readtime', 'created_at', 'update_at']

        read_only_fields = ['readtime', 'created_at', 'update_at']
        
    def get_readtime(self, obj):
        return obj.get_read_time()


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"