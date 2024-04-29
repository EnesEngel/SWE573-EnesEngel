from calendar import c
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from rest_framework.parsers import JSONParser
from .models import MembershipRequest, Owner, Post, PostFormat, User, UserProfile, Community, Follower, CommunityMember, Moderator, CommunityBannedUser, UserBlockedUser, Comment, Vote, FollowRequest
from .serializers import CommunitySerializer, FollowerSerializer, PostSerializer, UserProfileSerializer, OwnerSerializer, ModeratorSerializer, CommunityMemberSerializer, CommunityBannedUserSerializer, UserBlockedUserSerializer, VoteSerializer, CommentSerializer, PostFormatSerializer, MembershipRequestSerializer, FollowRequestSerializer
# from .forms import UserForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
# serializerlar yazılınca buraya ekleyeceğim from .serializers import UserSerializer, LoginSerializer
# Create your views here.

"""
# EE
default post template'ı unutma
user creation'ı değiştiricem
X user profile edit api view
login api view
X community creation api view
X community edit api view
X post Format creation api view
X post Format edit ama sadece deactivate/activate  api view
X post creation api view
X post edit ama sadece deactivate/activate  api view ?? emin değilim bakıcam
X community membership creation api view
X community membership edit api view
comment creation api view
vote api view both for comment and posts
follow api view
block api view
ban api view
reply membership request api view
reply follow request api view
moderator adding api view
moderator edit api view
"""


'''
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        password = request.POST.get('password')

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            is_private = form.cleaned_data['is_private']

            user = User.objects.create(
                username=username,
                email=email,
                password_hash=make_password(password),
                is_private=is_private
            )
            messages.success(request, 'User created successfully!')
            return redirect('home')
        else:
            err_str = ""
            for field in form:
                if field.errors:
                    err_str += field.name + " Already Exists.\n"
            messages.error(request, err_str)

    else:
        form = UserForm()
    return render(request, 'BoSApp/create_user.html', {'form': form})


def home(request):
    return render(request, 'BoSApp/home.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

       # try:
        # user = User.objects.get(username=username)
        # flash messages gelecek ve user modeli eklenmeli
    context = {}
    return render(request, 'BoSApp/login_register.html', context)
'''

# region htmlcalls


def home(request):
    return render(request, 'BoSApp/home.html')


def create_post_page_view(request):
    return render(request, 'BoSApp/create_post.html')


def create_posttype_page_view(request):
    return render(request, 'BoSApp/create_posttype.html')


def post_formats_page_view(request):
    return render(request, 'BoSApp/postTypes.html')


def create_user_view(request):

    return render(request, 'BoSApp/create_user.html')


def loginPage_view(request):
    return render(request, 'BoSApp/login.html')


def feed_view(request):
    return render(request, 'BoSApp/feed.html')


def single_community(request):
    community_id = request.GET.get('id', None)
    return render(request, 'single_community.html', {'community_id': community_id})


def profile_page_view(request):
    return render(request, 'BoSApp/profile.html')


def community_page_view(request):
    return render(request, 'BoSApp/community.html')


def create_community_view(request):
    return render(request, 'BoSApp/create_community.html')


def enrolled_communities_page_view(request):
    return render(request, 'BoSApp/enrolled_communities.html')


def enrolled_communities_view(request):
    if request.user.is_authenticated:
        community_memberships = CommunityMember.objects.filter(
            user=request.user, is_active=True)
        communities = [
            membership.community for membership in community_memberships]
        return render(request, 'BoSApp/enrolled_communities.html', {'communities': communities})
    else:
        return redirect('/login/')


def create_community_page_view(request):
    return render(request, 'BoSApp/create_community.html')


def owned_communities_view(request):
    return render(request, 'BoSApp/owned_communities.html')


def my_posts_view(request):
    return render(request, 'BoSApp/my_posts.html')


def single_community_page(request):
    return render(request, 'BoSApp/single_community.html')
# endregion

# region apiviews


def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return JsonResponse({'message': 'Logout successful'}, status=200)


@csrf_exempt  # Usually not recommended without additional security measures
@require_http_methods(["POST"])
def login_view(request):
    import json
    data = json.loads(request.body)
    username = data.get('user', {}).get('username')
    password = data.get('user', {}).get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def check_username(request):
    from django.http import JsonResponse
    import json

    data = json.loads(request.body)
    username = data.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'isAvailable': not exists})


@csrf_exempt
@require_http_methods(["POST"])
def check_email(request):
    from django.http import JsonResponse
    import json

    data = json.loads(request.body)
    email = data.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'isAvailable': not exists})

# endregion

# region viewsets


class UserCommunityViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        communities_list = CommunityMember.objects.filter(
            user=self.request.user)
        return [community.community for community in communities_list]


class OwnerCommunityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Community.objects.filter(owner_user=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class ModeratorViewSet(viewsets.ModelViewSet):
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializer


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer


class CommunityMemberViewSet(viewsets.ModelViewSet):
    queryset = CommunityMember.objects.all()
    serializer_class = CommunityMemberSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]


class CommunityBannedUserViewSet(viewsets.ModelViewSet):
    queryset = CommunityBannedUser.objects.all()
    serializer_class = CommunityBannedUserSerializer


class UserBlockedUserViewSet(viewsets.ModelViewSet):
    queryset = UserBlockedUser.objects.all()
    serializer_class = UserBlockedUserSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner_user=self.request.user)
        community = serializer.instance
        CommunityMember.objects.create(
            community=community, user=self.request.user, is_active=True)
        Owner.objects.create(community=community,
                             owner_user=self.request.user, is_active=True)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def user_role(self, request, pk=None):
        community = self.get_object()
        user = request.user
        is_owner = community.owner_user == user
        communityid = community.community_id
        print(communityid)
        print(user.id)
        is_member = CommunityMember.objects.filter(
            community=communityid, user=user).exists()
        return Response({'is_owner': is_owner, 'is_member': is_member})


class PostFormatViewSet(viewsets.ModelViewSet):
    queryset = PostFormat.objects.all()
    serializer_class = PostFormatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        community_id = self.request.query_params.get('community_id')
        print("communityId:"+community_id)
        if community_id is not None:
            queryset = queryset.filter(community__community_id=community_id)
        return queryset


class MembershipRequestViewSet(viewsets.ModelViewSet):
    queryset = MembershipRequest.objects.all()
    serializer_class = MembershipRequestSerializer


class FollowRequestViewSet(viewsets.ModelViewSet):
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer

# endregion
