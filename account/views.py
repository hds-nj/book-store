from multiprocessing import context
from django.contrib.auth import update_session_auth_hash

from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User 
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from .models import Profile
from .forms import *
from django.views import generic
@login_required(login_url='login')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name= 'edit_profil3e.html'
    success_url = reverse_lazy('home')
    def get_object(self):
        return self.request.user

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'home')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('profile')
        else:
            messages.success(
                request, 'An error has occurred during registration')
    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)
@login_required(login_url='login')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password/password.html', {
        'form': form
    })


@login_required(login_url='login')
def userAccount(request):
    profile = Profile.objects.all()
    context = {'p': profile}
    return render(request, 'account.html', context=context)


@login_required(login_url='login')
def editAccount(request):
  if request.method == "POST":
        form = EditProfileForm(request.user.username,request.POST, request.FILES)
        if form.is_valid():
            
            username= form.cleaned_data["username"]
            profile=User(username = username)
            profile.save()
  else:
        form = EditProfileForm(request.user.username)
  return render(request, 'edit-profile.html', {'form': form})
