from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, PasswordContextMixin, PasswordResetCompleteView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from .models import Profile


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        new_photo = request.FILES.get('photo')
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)

        if new_photo:
            profile.photo = new_photo
            profile.save()
            messages.success(request, 'Фото профиля успешно изменено!')

        return redirect(request.path)


class UsersView(ListView):
    template_name = 'myauth/users.html'
    context_object_name = 'users'
    queryset = User.objects.all()


class UserDetailsView(DetailView):
    template_name = 'myauth/user.html'
    model = User
    context_object_name = 'user'

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        new_photo = request.FILES.get('photo')

        try:
            profile = Profile.objects.get(user=self.object)
        except Profile.DoesNotExist:
            profile = Profile(user=self.object)

        if new_photo:
            profile.photo = new_photo
            profile.save()
            messages.success(request, 'Фото профиля успешно изменено!')

        return redirect(request.path)


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        login(request=self.request, user=user)
        return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {'error': 'Invalid username or password.'})


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie("Kirill", "Losev", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('Kirill', 'no-cookies')
    return HttpResponse(f'Cookie value: {value!r}')


def del_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie cleared!')
    response.delete_cookie('Kirill')
    return response


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Set session!')


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session: {value!r}')


def del_session_view(request: HttpRequest) -> HttpResponse:
    request.session.clear()
    return HttpResponse('Session deleted!')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})
