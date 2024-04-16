from utils.api import APIView, validate_serializer
from ..serializers import CreateReplySerializer, CreateDiscussionSerializer, EditDiscussionSerializer, DiscussionSerializer, CreateCommentSerializer
from discussion.models import Discussion, Comment, Replay
from account.decorators import login_required

class DiscussionAPI(APIView):
    @login_required
    @validate_serializer(CreateDiscussionSerializer)
    def post(self, request):
        data = request.data
        current_user = request.user
        if not current_user.is_admin_role():
            data["top_priority"] = False
        data["author"] = current_user
        Discussion.objects.create(**data)
        return self.success()
    
    @login_required
    def delete(self, request):
        did = request.GET.get("did")
        try:
            discussion = Discussion.objects.get(id=did)
            if not request.user.is_admin_role() and discussion.author.username != request.user.username:
                return self.error("Permission denied")
            discussion.delete()
            return self.success()
        except Discussion.DoesNotExist:
            return self.error("discussion not found")
    
    @login_required
    @validate_serializer(EditDiscussionSerializer)
    def put(self, request):
        data = request.data
        current_user = request.user
        if not current_user.is_admin_role():
            data["top_priority"] = False
        try:
            discussion = Discussion.objects.get(id=data["id"])
            if discussion.author.username != current_user.username:
                return self.error("Permission denied")
            for k, v in data.items():
                setattr(discussion, k, v)
            discussion.save()
            return self.success()
        except Discussion.DoesNotExist:
            return self.error("discussion not found")
    
    def get(self, request):
        did = request.GET.get("did")
        if did:
            try:
                discussion = Discussion.objects.get(id=did)
                # 浏览量+1
                discussion.views += 1
                discussion.save()
                return self.success(DiscussionSerializer(discussion, need_comments=True).data)
            except Discussion.DoesNotExist:
                return self.error("discussion not found")
        keyword = request.GET.get("keyword")
        ordering = request.GET.get("ordering")
        if keyword:
            discussions = Discussion.objects.filter(title__icontains=keyword)
        else:
            discussions = Discussion.objects.all()
        if ordering:
            discussions = discussions.order_by('-top_priority', ordering)
        else:
            discussions = discussions.order_by('-top_priority', '-created_at')
        return self.success(self.paginate_data(request, discussions, DiscussionSerializer))


class CommentAPI(APIView):
    @login_required
    @validate_serializer(CreateCommentSerializer)
    def post(self, request):
        data = request.data
        current_user = request.user
        data["author"] = current_user
        try:
            discussion = Discussion.objects.get(id=data["discussion_id"])
            data["discussion"] = discussion
            Comment.objects.create(**data)
            return self.success()
        except Discussion.DoesNotExist:
            return self.error("discussion not found")
    

    @login_required
    def delete(self, request):
        cid = request.GET.get("cid")
        try:
            comment = Comment.objects.get(id=cid)
            if not request.user.is_admin_role() and comment.author.username != request.user.username:
                return self.error("Permission denied")
            comment.delete()
            return self.success()
        except Comment.DoesNotExist:
            return self.error("comment not found")


class ReplyAPI(APIView):
    @login_required
    @validate_serializer(CreateReplySerializer)
    def post(self, request):
        data = request.data
        current_user = request.user
        data["from_user"] = current_user
        try:
            comment = Comment.objects.get(id=data["comment_id"])
            data["comment"] = comment
            Replay.objects.create(**data)
            return self.success()
        except Comment.DoesNotExist:
            return self.error("comment not found")
        except:
            return self.error("request error")
    

    @login_required
    def delete(self, request):
        rid = request.GET.get("rid")
        try:
            reply = Replay.objects.get(id=rid)
            if not request.user.is_admin_role() and reply.from_user.username != request.user.username:
                return self.error("Permission denied")
            reply.delete()
            return self.success()
        except Replay.DoesNotExist:
            return self.error("reply not found")
