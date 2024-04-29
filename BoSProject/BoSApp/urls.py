from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import OwnerCommunityViewSet, UserCommunityViewSet, UserProfileViewSet, CommunityViewSet, PostViewSet, FollowerViewSet, CommentViewSet, UserViewSet, VoteViewSet, OwnerViewSet, ModeratorViewSet, CommunityMemberViewSet, CommunityBannedUserViewSet, UserBlockedUserViewSet, PostFormatViewSet, MembershipRequestViewSet, FollowRequestViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
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
router.register(r'my-communities', UserCommunityViewSet,
                basename='my-communities')
router.register(r'owned-communities', OwnerCommunityViewSet,
                basename='owned-communities')

urlpatterns = [
    path('', include(router.urls)),
    path('api/check_username/', views.check_username, name='check_username'),
    path('api/check_email/', views.check_email, name='check_email'),
    path('create_user/', views.create_user_view, name='create_user'),
    path('home', views.home, name="home"),
    path('loginPage/', views.loginPage_view, name="loginPage"),
    path('feed/', views.feed_view, name="feed"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.profile_page_view, name="profile"),
    path('community/', views.community_page_view, name="community"),
    path('create_community/', views.create_community_view, name="create_community"),
    path('enrolled_communities/', views.enrolled_communities_view,
         name="enrolled_communities"),
    path('enrolled_communities_page/', views.enrolled_communities_page_view,
         name="enrolled_communities_page"),
    path('owned_communities/', views.owned_communities_view,
         name="owned_communities"),
    path('my_posts/', views.my_posts_view, name="my_posts"),
    path('single_community/', views.single_community_page,
         name='single_community'),
    path('create_community_page/', views.create_community_page_view,
         name='create_community_page'),
    path('create_posttype_page/', views.create_posttype_page_view,
         name='create_posttype_page'),
    path('create_post_page/', views.create_post_page_view, name='create_post_page'),

    # path('create/', views.create_user, name='create_user'),
]
