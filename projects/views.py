from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import search_project, paginate_project


@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()
    profile = request.user.profile

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid:
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, 'create_project.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context = {
        'form': form,
        'project': project
    }
    return render(request, 'create_project.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {
        'object': project
    }
    return render(request, 'delete-template.html', context)


def projects(request):
    projects, search_query = search_project(request)

    custom_range, projects = paginate_project(request, projects, 6)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range
    }
    return render(request, 'projects.html', context)


def project(request, pk):
    project_obj = get_object_or_404(Project, id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project_obj
        review.owner = request.user.profile
        review.save()

        project_obj.get_vote_count

        messages.success(request, 'Your review was successfully submitted')
        return redirect('project', pk=project_obj.id)

    context = {
        'project': project_obj,
        'form': form,
    }
    return render(request, 'project.html', context)
