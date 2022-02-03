from django.shortcuts import render, redirect, get_object_or_404
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from .utils import search_project, paginate_project


@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()
    profile = request.user.profile

    if request.method == 'POST':
        # newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid:
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            # for tag in newtags:
            #     tag, created = Tag.objects.get_or_create(name=tag)
            return redirect('account')

    context = {'form': form}
    return render(request, 'create_project.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {
        'form': form
    }
    return render(request, 'update_project.html', context)


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

    context = {
        'project': project_obj
    }

    return render(request, 'project.html', context)
