from django.db import models

class Discussion(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=511)
    content = models.TextField()
    author = models.ForeignKey('account.User', on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    top_priority = models.BooleanField(default=False)
    status = models.IntegerField(default=0) # 0: normal, 1: banned
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'discussion'
        ordering = ['-top_priority', '-created_at']


class Comment(models.Model):
    content = models.TextField()
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    author = models.ForeignKey('account.User', on_delete=models.CASCADE)
    status = models.IntegerField(default=0) # 0: normal, 1: banned
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comment'
        ordering = ['-created_at']


class Replay(models.Model):
    content = models.TextField()
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    from_user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='to_user')
    status = models.IntegerField(default=0) # 0: normal, 1: banned
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'replay'
