from random import randint

from django.views.generic import FormView, View
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignupForm, LoginForm, CompleteSignup
from .models import User


class SignUpView(FormView):
    template_name = 'register.html'
    form_class = SignupForm

    def form_valid(self, form):
        if not form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
            form.add_error('confirm_password', "Password doesn't match")
            return self.form_invalid(form)
        user = User.objects.create_user(email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        date_of_birth=form.cleaned_data['date_of_birth'])
        login(self.request, user)
        return HttpResponseRedirect(reverse('auth:complete_signup', args=[user.pk]))


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(self.request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        if not user:
            form.add_error('', "Invalid email or password!")
            return self.form_invalid(form)
        login(self.request, user)
        return HttpResponseRedirect(reverse('core:dashboard'))


class LogoutView(View):

    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('auth:login'))


class CompleteSignupView(FormView, LoginRequiredMixin):
    form_class = CompleteSignup
    login_url = reverse_lazy('auth:login')
    template_name = 'complete-signup.html'

    def get_context_data(self, **kwargs):
        context = super(CompleteSignupView, self).get_context_data(**kwargs)
        ids = list(self.request.user.friends.all().values_list("pk", flat=True))
        ids.append(self.request.user.pk)
        users = User.objects.all().order_by("created_at").exclude(id__in=ids)
        if users.count() < 10:
            context['suggested_friends'] = users
            return context

        suggested_friends = []
        for i in range(10):
            random_index = randint(0, users.count())
            suggested_friends.append(users[random_index])

        context['suggested_friends'] = suggested_friends
        return context

    def form_valid(self, form):
        city = form.cleaned_data['city'].capitalize()
        country = form.cleaned_data['country'].capitalize()
        picture = form.cleaned_data['profile_picture']
        user = User.objects.get(pk=self.kwargs.get('user_id'))
        user.city = city
        user.country = country
        user.image = picture
        user.save()
        return HttpResponseRedirect(reverse('core:dashboard'))
