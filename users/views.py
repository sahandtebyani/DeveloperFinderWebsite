from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import search_profile, paginate_profile


def login_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = get_object_or_404(User, username=username)
        except:
            messages.error(request, 'user does not exists')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/user-login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    else:
        form = CustomUserCreationForm()
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.email = user.username
                user.first_name = user.first_name.capitalize()
                user.last_name = user.last_name.capitalize()
                user.save()

                messages.success(request, 'User account was created')

                login(request, user)
                return redirect('edit-account')
            else:
                messages.error(request, 'An error occurred during registration')

        context = {
            'form': form
        }
        return render(request, 'users/user-register.html', context)


def profiles(request):
    profiles, search_query = search_profile(request)

    custom_range, profiles = paginate_profile(request, profiles, 3)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = get_object_or_404(Profile, id=pk)

    """ top_skills are that have description"""
    top_skills = profile.skill_set.exclude(description__exact="")
    other_skills = profile.skill_set.filter(description__iexact="")

    context = {
        'profile': profile,
        'topskills': top_skills,
        'otherskills': other_skills
    }
    return render(request, 'users/user_profile.html', context)


@login_required(login_url='login')
def user_account(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
    context = {
        'form': form
    }
    return render(request, 'users/profile-form.html', context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully')
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def edit_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully')
        return redirect('account')
    context = {
        'object': skill
    }
    return render(request, 'delete-template.html', context)
