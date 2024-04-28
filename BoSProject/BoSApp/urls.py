from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, CommunityViewSet, PostViewSet, FollowerViewSet, CommentViewSet, VoteViewSet, OwnerViewSet, ModeratorViewSet, CommunityMemberViewSet, CommunityBannedUserViewSet, UserBlockedUserViewSet, PostFormatViewSet, MembershipRequestViewSet, FollowRequestViewSet

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'owners', OwnerViewSet)
router.register(r'moderators', ModeratorViewSet)
router.register(r'followers', FollowerViewSet)
router.register(r'communitymembers', CommunityMemberViewSet)
router.register(r'communitybannedusers', CommunityBannedUserViewSet)
router.register(r'userblockedusers', UserBlockedUserViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'communities', CommunityViewSet)
router.register(r'postformats', PostFormatViewSet)
router.register(r'membershiprequests', MembershipRequestViewSet)
router.register(r'followrequests', FollowRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/check_username/', views.check_username, name='check_username'),
    path('api/check_email/', views.check_email, name='check_email'),
    path('create_user/', views.create_user_view, name='create_user'),
    path('home', views.home, name="home"),
    path('login/', views.home, name="login"),
    # path('create/', views.create_user, name='create_user'),
]
