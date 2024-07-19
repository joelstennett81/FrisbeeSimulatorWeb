from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DetailView

from frisbee_simulator_web.forms import LoginForm, ProfileForm
from frisbee_simulator_web.models import Profile


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # create a new Profile instance for the user
            login(request, user)
            return redirect('home')
            # return redirect('/profile/edit/')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/view_profile.html'

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'users/edit_profile.html'
    success_url = '/profile/view/'

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


# logout page
def user_logout(request):
    logout(request)
    return redirect('login')
