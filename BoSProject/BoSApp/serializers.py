from calendar import c
from django.contrib.auth.models import User
from .models import Community, Follower, Post, UserProfile, CommunityMember, CommunityBannedUser, UserBlockedUser, Vote, Comment, Owner, Moderator, PostFormat, MembershipRequest, FollowRequest
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import base64
from django.core.files.base import ContentFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'image', 'is_private', 'created_date', 'is_active']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        user_profile = UserProfile.objects.create(user=user, **validated_data)
        image_data = validated_data.pop('image', None)
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(base64.b64decode(imgstr),
                                name=f'user_{user.pk}.{ext}')

            user_profile = UserProfile.objects.create(
                user=user, image=image, **validated_data)
        else:
            user_profile = UserProfile.objects.create(
                user=user, **validated_data)

        return user_profile


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'


class CommunityMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityMember
        fields = '__all__'


class CommunityBannedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityBannedUser
        fields = '__all__'


class UserBlockedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBlockedUser
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class ModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderator
        fields = '__all__'


class PostFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFormat
        fields = '__all__'


class MembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = '__all__'


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = '__all__'
