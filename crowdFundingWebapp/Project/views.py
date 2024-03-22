from .forms import CategoryForm, ProjectForm, ProjectImageForm, TagForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Project, ProjectImage, Tag
from django.contrib.auth.decorators import login_required
from authentication.models import CustomUser


# Create your views here.
@login_required
def create_category(request):
    categories = Category.objects.all()
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            if Category.objects.filter(name=category_name).exists():
                form.add_error('name', 'Category with this name already exists.')
            else:
                form.save()
                return redirect('create_category')
    return render(request, 'admin/create_category.html', {'categories': categories, 'form': form})


@login_required
def select_featured_projects(request):
    print(1)


# def list_latest_featured_projects(request):
#     # featured_projects = Project.objects.filter(is_featured=True).order_by('-created_at')[:5]
#     # return render(request, 'admin/latest_featured_projects.html', {'featured_projects': featured_projects})
#     print(1)

# def list_categories(request):
#     # categories = Category.objects.all()
#     # return render(request, 'admin/list_categories.html', {'categories': categories})
#     print(1)



def project_list(request):
    projects = Project.objects.all()
    print("Number of projects:", len(projects))  # Debugging line to print the number of projects
    return render(request, 'Project/project_list.html', {'projects': projects})
#========================================================================================================================
# CRUD operations
#========================================================================================================================




@login_required
def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        image_form = ProjectImageForm(request.POST, request.FILES)
        tag_form = TagForm(request.POST)  # Instantiate TagForm here

        if project_form.is_valid() and image_form.is_valid() and tag_form.is_valid():
            project = project_form.save(commit=False)
            user_id = request.user.id
            creator = get_object_or_404(CustomUser, id=user_id)
            project.creator = creator
            project.save()

            # Save project images
            for image in request.FILES.getlist('image'):
                ProjectImage.objects.create(project=project, image=image)

            # Save project tags
            tags = tag_form.cleaned_data.get('name', [])
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                project.tags.add(tag)

            return redirect('project_detail', project_id=project.id)
    else:
        project_form = ProjectForm()
        image_form = ProjectImageForm()
        tag_form = TagForm()  # Instantiate TagForm here

    return render(request, 'projects/create_project.html', {'project_form': project_form, 'image_form': image_form, 'tag_form': tag_form})


# @login_required
# def create_project(request):
#     if request.method == 'POST':
#         project_form = ProjectForm(request.POST)
#         image_form = ProjectImageForm(request.POST, request.FILES)
#         tag_form = TagForm(request.POST)  # Instantiate TagForm here
#         if project_form.is_valid():
#             project = project_form.save(commit=False)
#             user_id = request.user.id
#             creator = get_object_or_404(CustomUser, id=user_id)
#             project.creator = creator
#             project.save()
#             # Save project images
#             for image in request.FILES.getlist('image'):
#                 ProjectImage.objects.create(project=project, image=image)
#
#             # Save project tags
#             tags = tag_form.cleaned_data['name']
#             for tag_name in tags:
#                 tag, _ = Tag.objects.get_or_create(name=tag_name)
#                 project.tags.add(tag)
#
#             return redirect('project_detail', project_id=project.id)
#     else:
#         project_form = ProjectForm()
#         image_form = ProjectImageForm()
#         tag_form = TagForm()  # Instantiate TagForm here
#
#     return render(request, 'create_project.html',
#                   {'project_form': project_form, 'image_form': image_form, 'tag_form': tag_form})
#

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, creator=request.user)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
            project = project_form.save()
            return redirect('project_detail', project_id=project.id)
    else:
        project_form = ProjectForm(instance=project)
    return render(request, 'projects/update_project.html', {'project_form': project_form})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, creator=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('user_projects')
    return render(request, 'projects/delete_project.html', {'project': project})

@login_required
def user_projects(request):
    projects = Project.objects.filter(creator=request.user)
    return render(request, 'projects/user_projects.html', {'projects': projects})

def home(request):
    return render(request, 'Home/home.html')


def search(request):
    return render(request, 'Home/search.html')
