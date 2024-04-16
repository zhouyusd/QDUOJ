from django.conf.urls import url

from ..views.oj import DiscussionAPI, CommentAPI, ReplyAPI

urlpatterns = [
    url(r"^discussion/?$", DiscussionAPI.as_view(), name="discussion_api"),
    url(r"^discussion/comment/?$", CommentAPI.as_view(), name="comment_api"),
    url(r"^discussion/reply/?$", ReplyAPI.as_view(), name="reply_api"),
]
