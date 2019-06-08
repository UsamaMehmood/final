import uuid

from django.db import models


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    by = models.ForeignKey('authentication.User', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"

    def __str__(self):
        return "Liked by: {} {}".format(self.by.first_name, self.by.last_name)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    message = models.CharField(max_length=500)
    commenter = models.ForeignKey(to='authentication.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Like)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return "{} By: {} {}".format(self.message, self.commenter.first_name, self.commenter.last_name)

    def add_like(self, user):
        self.likes.add(Like.objects.create(on="comment", by=user))
        self.save()


class Share(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    shared_by = models.ForeignKey('authentication.User', on_delete=models.PROTECT)
    message = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Share"
        verbose_name_plural = "Shares"

    def __str__(self):
        return "Shared by: {} {}".format(self.shared_by.first_name, self.shared_by.last_name)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    caption = models.CharField(max_length=800)
    post_image = models.ImageField(upload_to="posts", null=True, blank=True)
    public = models.BooleanField(default=True)
    poster = models.ForeignKey(to='authentication.User', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(Like)
    comments = models.ManyToManyField(Comment)
    shares = models.ManyToManyField(Share)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return "Posted By: {} {}".format(self.poster.first_name, self.poster.last_name)

    def add_like(self, user):
        self.likes.add(Like.objects.create(on="post", by=user))
        self.save()


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('post_like', 'Liked a post'),
        ('post_comment', 'Commented on post'),
        ('post_share', 'Shared a post'),
        ('friend_request', 'Recieved a friend request'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(choices=NOTIFICATION_TYPES, max_length=15)
    by = models.ForeignKey('authentication.User', on_delete=models.PROTECT)
    seen = models.BooleanField(default=False)
    post_id = models.ForeignKey(Post, null=True, blank=True, default=None, on_delete=models.PROTECT)
