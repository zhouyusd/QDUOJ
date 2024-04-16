from utils.api import UsernameSerializer, serializers
from discussion.models import Discussion, Comment, Replay

class CreateDiscussionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=511)
    content = serializers.CharField()
    top_priority = serializers.BooleanField()


class CreateCommentSerializer(serializers.Serializer):
    content = serializers.CharField()
    discussion_id = serializers.IntegerField()


class CreateReplySerializer(serializers.Serializer):
    content = serializers.CharField()
    comment_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()


class EditDiscussionSerializer(CreateDiscussionSerializer):
    id = serializers.IntegerField()


class ReplaySerializer(serializers.ModelSerializer):
    from_user = UsernameSerializer()
    to_user = UsernameSerializer()

    class Meta:
        model = Replay
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = UsernameSerializer()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
    
    def get_replies(self, obj):
        replies = Replay.objects.filter(comment=obj)
        return ReplaySerializer(replies, many=True).data


class DiscussionSerializer(serializers.ModelSerializer):
    author = UsernameSerializer()
    comment_count = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Discussion
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        self.need_comments = kwargs.pop("need_comments", False)
        super().__init__(*args, **kwargs)

    def get_comment_count(self, obj):
        return Comment.objects.filter(discussion=obj).count()
    
    def get_comments(self, obj):
        if self.need_comments:
            comments = Comment.objects.filter(discussion=obj)
            return sorted(CommentSerializer(comments, many=True).data, key=lambda x: (len(x["replies"]), x["created_at"]), reverse=True)
        return []
