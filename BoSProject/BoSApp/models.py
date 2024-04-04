from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

'''
timezone'U nerenin timezone'u yapsam,
help_text diye bi şey varmiş
Verbose field names
json ve jsonb var
metadata var
'''

# region User Types


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_private = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)


class Owner(models.Model):
    owner_user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='owned_communities')
    community = models.ForeignKey(
        'Community', on_delete=models.CASCADE, related_name='owners')
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)


class Moderator(models.Model):
    moderator_user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='moderated_communities')
    community = models.ForeignKey(
        'Community', on_delete=models.CASCADE, related_name='moderators')
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)


class Follower(models.Model):
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='followers')
    follower_user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='following')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)


class CommunityMember(models.Model):
    community = models.ForeignKey(
        'Community', on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='communities')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)


class CommunityBannedUser(models.Model):  # banned from community
    community_id = models.ForeignKey('Community', on_delete=models.CASCADE)
    banned_user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    banning_moderator_user_id = models.ForeignKey(
        'User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)


class UserBlockedUser(models.Model):  # blocked by a user
    user_id = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='blocked')
    blocked_user_id = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='blocker')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)

# endregion

# region Interaction


class Vote(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=[(1, '+1'), (-1, '-1')])
    voted_content_type = models.SmallIntegerField(
        choices=[(1, 'Post'), (2, 'Comment')])
    voted_content_id = models.PositiveIntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    community_id = models.ForeignKey('Community', on_delete=models.CASCADE)
    post_format_id = models.ForeignKey('PostFormat', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = JSONField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    content = JSONField()  # stringle çalıştırsam yeter şimdilik ama ilerde kolaylık olur
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
# endregion

# region Community


class Community(models.Model):
    community_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner_user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)


class PostFormat(models.Model):
    post_format_id = models.AutoField(primary_key=True)
    format_type = models.JSONField()
    community_id = models.ForeignKey('Community', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)


# endregion

# region Requests

class MembershipRequest(models.Model):
    community_id = models.ForeignKey(
        'Community', on_delete=models.CASCADE, related_name='membership_requesting_user')
    Membership_requesting_user_id = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='membership_requested_community')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)


class FollowRequest(models.Model):
    user_id = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='follower_request_sending_user')
    follow_requesting_user_id = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='follower_request_receiving_user')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
