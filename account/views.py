from multiprocessing import context
from django.contrib.auth import update_session_auth_hash
from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import CreateView ,UpdateView,DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from .models import Profile
from .forms import *
from django.views import generic
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

authentication_classes = (TokenAuthentication,)
permission_classes = (IsAuthenticated,)
class ShowProfilePageView(DetailView):
    model = Profile
    template_name = "user-profile.html"

    def get_context_data(self, *args,**kwargs):
        users  = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data()
        page_user = get_object_or_404(Profile , id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context

class EditProfileView(UpdateView):
    model = Profile 
    form_class = ProfileUpdateForm
    template_name = 'edit_profile.html'
    def get_object(self , *args , **kwargs):
        user = get_object_or_404(User , pk=self.kwargs['pk'])
        return user.profile
    def get_success_url(self, *args, **kwargs):
        return reverse("home")     

# class UserEditView(generic.UpdateView):
#     form_class = EditProfileForm
#     template_name= 'edit_profile.html'
#     success_url = reverse_lazy('home')
#     def get_object(self):
#         return self.request.user

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
            Profile.objects.create(user=user)
            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('home')
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


