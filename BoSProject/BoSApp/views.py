from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import MembershipRequest, Owner, Post, PostFormat, User, UserProfile, Community, Follower, CommunityMember, Moderator, CommunityBannedUser, UserBlockedUser, Comment, Vote, FollowRequest
from .serializers import CommunitySerializer, FollowerSerializer, PostSerializer, UserProfileSerializer, OwnerSerializer, ModeratorSerializer, CommunityMemberSerializer, CommunityBannedUserSerializer, UserBlockedUserSerializer, VoteSerializer, CommentSerializer, PostFormatSerializer, MembershipRequestSerializer, FollowRequestSerializer
# from .forms import UserForm
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

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


def create_user_view(request):

    return render(request, 'BoSApp/create_user.html')

# endregion

# region apiviews


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



class UserProfileViewSet(viewsets.ModelViewSet):
    print("userprofileviewset")
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


class PostFormatViewSet(viewsets.ModelViewSet):
    queryset = PostFormat.objects.all()
    serializer_class = PostFormatSerializer


class MembershipRequestViewSet(viewsets.ModelViewSet):
    queryset = MembershipRequest.objects.all()
    serializer_class = MembershipRequestSerializer


class FollowRequestViewSet(viewsets.ModelViewSet):
    queryset = FollowRequest.objects.all()
    serializer_class = FollowRequestSerializer

# endregion
