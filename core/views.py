from random import randint

from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect

from authentication.models import User

from .models import Notification, Post


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = reverse_lazy('auth:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponseRedirect(self.login_url)

        if request.user.city == "" and request.user.country == "":
            return HttpResponseRedirect(reverse("auth:complete_signup", args=[request.user.pk]))

        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        if not self.request.user.friends.all().exists():
            ids = list(User.objects.filter(notifications__by=self.request.user, notifications__type='friend_request')
                       .values_list("pk", flat=True))
        else:
            ids = list(self.request.user.friends.all().values_list("pk", flat=True))
        ids.append(self.request.user.pk)
        context['posts'] = Post.objects.filter(poster_id__in=ids).order_by('-created_at')
        users = User.objects.all().order_by("created_at").exclude(id__in=ids)
        if users.count() < 5:
            context['suggested_friends'] = users
            return context

        suggested_friends = []
        for i in range(5):
            random_index = randint(0, users.count()-1)
            suggested_friends.append(users[random_index])

        context['suggested_friends'] = suggested_friends
        return context


class NotificationView(DetailView, LoginRequiredMixin):
    template_name = 'notification.html'
    model = Notification
    context_object_name = 'notification'

    def get(self, request, *args, **kwargs):
        response = super(NotificationView, self).get(request, *args, **kwargs)
        self.object.seen = True
        self.object.save()
        return response

    def get_context_data(self, **kwargs):
        context = super(NotificationView, self).get_context_data(**kwargs)
        ids = list(self.request.user.friends.all().values_list("pk", flat=True))
        ids.append(self.request.user.pk)
        users = User.objects.all().order_by("created_at").exclude(id__in=ids)
        if users.count() < 5:
            context['suggested_friends'] = users
            return context

        suggested_friends = []
        for i in range(5):
            random_index = randint(0, users.count() - 1)
            suggested_friends.append(users[random_index])

        context['suggested_friends'] = suggested_friends
        return context

    def post(self, request, *args, **kwargs):
        status = request.POST['status']
        obj = self.get_object(self.get_queryset())
        if status == 'approved':
            request.user.friends.add(obj.by)
            obj.by.friends.add(request.user)
            request.user.save()
            obj.by.save()

        return HttpResponseRedirect(reverse('core:dashboard'))


class SearchResults(View, LoginRequiredMixin):
    http_method_names = ['post']

    def post(self, request):
        query = request.POST['query']
        context = dict()
        context['search_results'] = User.objects.filter(Q(first_name__contains=query) | Q(last_name__contains=query)
                                                        | Q(city__contains=query) | Q(country__contains=query))

        context['search_query'] = query

        context['user_friends'] = request.user.friends.all().values_list("pk", flat=True)

        return render(request, 'search.html', context)


class FriendsSuggestionView(LoginRequiredMixin, TemplateView):
    template_name = 'friends-suggestion.html'

    def get_context_data(self, **kwargs):
        context = super(FriendsSuggestionView, self).get_context_data(**kwargs)
        user_friends_ids = self.request.user.friends.values_list('id', flat=True)
        context['nearby_friends'] = User.objects.filter(
            Q(city=self.request.user.city) | Q(country=self.request.user.country))\
            .distinct().exclude(id__in=user_friends_ids).exclude(id=self.request.user.id)

        ids = []
        for friend in self.request.user.friends.all():
            for id in friend.friends.all().values_list('id', flat=True):
                if id not in ids:
                    ids.append(id)

        context['friends_of_friends'] = User.objects.filter(id__in=ids).distinct().exclude(id=self.request.user.id)
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    model = User
    context_object_name = 'obj'
    login_url = reverse_lazy('auth:login')

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        posts_current_user = Post.objects.filter(poster=context['obj'])
        if context['obj'] not in self.request.user.friends.all():
            posts_current_user = posts_current_user.filter(public=True)

        context['posts'] = posts_current_user

        is_friend = context['obj'] in self.request.user.friends.all()
        friend_request_sent = self.request.user.notifications.filter(by=context['obj'], seen=False) \
                              or context['obj'].notifications.filter(by=self.request.user, seen=False)
        context['is_friend'] = is_friend or friend_request_sent

        mutual_friends = []
        for friend in context['obj'].friends.all():
            if friend in self.request.user.friends.all():
                mutual_friends.append(friend)

        context['mutual_friends'] = mutual_friends
        return context
