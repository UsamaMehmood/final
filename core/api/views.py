import base64
from datetime import datetime

from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.files.base import ContentFile
from django.db.models import Q

from core.models import Notification, Post, Like, Comment, Share
from authentication.models import User
from .serializers import NotificationsSerializer, UserMiniSerializer


class SendFriendRequest(View):
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SendFriendRequest, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        user = User.objects.get(pk=request.POST['to'])
        for notification in user.notifications.all():
            if notification.by_id == request.POST["from"] and notification.type == "friend_request":
                return JsonResponse({"status": "success"})
        notification = Notification.objects.create(type="friend_request", by_id=request.POST['from'])
        user.notifications.add(notification)
        user.save()

        return JsonResponse({"status": "success"})


class NotificationsView(APIView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationsView, self).dispatch(request, *args, **kwargs)

    def get(self, _request, *_args, **kwargs):
        user = User.objects.get(pk=kwargs.get("user_id"))
        notifications = NotificationsSerializer(user.notifications.filter(seen=False), many=True).data
        return Response(notifications)


class CreatePost(APIView):
    http_method_names = ['post']
    authentication_classes = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CreatePost, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        image = request.POST.get('image')
        caption = request.POST.get('caption')
        public = request.POST.get('status')
        poster = request.POST.get('post_by')

        post = Post()
        post.poster_id = poster
        post.caption = caption
        post.public = public == "public"
        post.save()
        if image != "":
            type, content = image.split(";base64,")
            _, ext = type.split('/')
            image = ContentFile(base64.b64decode(content), "{}.{}".format(post.id, ext))
            post.post_image = image
            post.save()

        return Response("success")


class LikeApi(APIView):
    http_method_names = ['post']
    authentication_classes = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(LikeApi, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_id = request.POST['post_id']
        user_id = request.POST['user_id']

        like = Like.objects.create(by_id=user_id)
        post = Post.objects.get(pk=post_id)
        post.likes.add(like)
        post.save()

        notification = Notification.objects.create(type="post_like", by_id=user_id, post_id=post)
        post.poster.notifications.add(notification)
        post.poster.save()

        return Response({"status": "success"})


class UnlikeApi(APIView):
    http_method_names = ['post']
    authentication_classes = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(UnlikeApi, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_id = request.POST['post_id']
        user_id = request.POST['user_id']

        post = Post.objects.get(pk=post_id)
        like = post.likes.get(by_id=user_id)
        post.likes.remove(like)
        post.save()

        return Response({"status": "success"})


class CommentApi(APIView):
    http_method_names = ['post']
    authentication_classes = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(CommentApi, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        message = request.POST['message']
        post_id = request.POST['post_id']
        user_id = request.POST['user_id']

        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(commenter_id=user_id, message=message)
        post.comments.add(comment)
        post.save()

        notification = Notification.objects.create(type="post_comment", by_id=user_id, post_id=post)
        post.poster.notifications.add(notification)
        post.poster.save()

        return Response({"status": "success"})


class SharePostApi(APIView):
    http_method_names = ['post']
    authentication_classes = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SharePostApi, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        post_id = request.POST['post_id']
        user_id = request.POST['user_id']
        message = request.POST['message']

        post = Post.objects.get(id=post_id)

        share = Share.objects.create(shared_by_id=user_id, message=message)
        post.shares.add(share)
        post.save()

        notification = Notification.objects.create(type="post_share", by_id=user_id, post_id=post)
        post.poster.notifications.add(notification)
        post.poster.save()

        return Response({"status": "success"})


class SearchAPI(APIView):
    http_method_names = ['post']
    authentication_classes = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(SearchAPI, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        query = request.POST['query']

        users = UserMiniSerializer(User.objects.filter(Q(first_name__contains=query) | Q(last_name__contains=query)
                                                       | Q(city__contains=query) | Q(country__contains=query)),
                                   many=True).data

        return Response(users)


class EditProfileApi(APIView):
    http_method_names = ['post']
    authentication_classes = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(EditProfileApi, self).dispatch(request, *args, **kwargs)

    def post(self, request, *_args, **kwargs):
        user = User.objects.get(pk=kwargs.get("pk"))
        first_name = request.POST.get("first_name", user.first_name)
        last_name = request.POST.get("last_name", user.last_name)
        dob = request.POST.get("dob", user.date_of_birth)
        email = request.POST.get("email", user.email)

        if first_name == '':
            first_name = user.first_name

        if last_name == '':
            last_name = user.last_name

        if dob == '':
            dob = user.date_of_birth

        if email == '':
            email = user.email

        dob = datetime(dob).strftime("YYYY-MM-DD")

        try:
            user.first_name = first_name
            user.last_name = last_name
            user.date_of_birth = dob
            user.email = email
            user.save()
        except:
            return Response({"status": "failed"})

        return Response({"status": "success"})
