from django.shortcuts import render,redirect
from project.forms import CategoryForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin/create_category.html', {'form': form})

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