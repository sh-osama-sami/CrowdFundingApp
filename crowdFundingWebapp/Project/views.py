from django import forms
from .forms import CategoryForm, DonationForm, ProjectForm, ProjectImageForm, TagForm, CommentForm, ReportForm, \
    ReportCommentForm, \
    UpdateProjectImageForm, UpdateTagForm, RatingForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Project, ProjectImage, Tag, Report, Comment, ReportComment, Rating
from django.contrib.auth.decorators import login_required
from authentication.models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Avg, Q
from django.contrib import messages


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
    else:
        form = CategoryForm()
    return render(request, 'admin/create_category.html', {'categories': categories, 'form': form})


@login_required
def select_featured_projects(request):
    projects = Project.objects.all()
    categories = Category.objects.all()
    return render(request, 'admin/featured_project.html', {'projects': projects, 'categories': categories})


@csrf_exempt
def update_featured_status(request, project_id):
    if request.method == 'POST':
        try:
            project = Project.objects.get(pk=project_id)
            if project.is_featured:
                project.is_featured = False
                project.save()
                return JsonResponse({'success': True, 'message': 'Project unfeatured'})
            else:
                featured_projects_count = Project.objects.filter(is_featured=True).count()
                if featured_projects_count < 5:
                    project.is_featured = True
                    project.save()
                    return JsonResponse({'success': True, 'message': 'Project featured'})
                else:
                    return JsonResponse({'success': False, 'error': 'Cannot feature more than 5 projects'}, status=400)
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Project does not exist'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


# @login_required
# def admin_home(request):
#     active_projects_count = Project.objects.filter(is_active=1)
#     non_active_projects_count = Project.objects.filter(is_active=0).count()
#     print("count: ",active_projects_count)
#     return render(request, 'admin/admin_home.html', {'active_projects_count': active_projects_count, 'non_active_projects_count': non_active_projects_count})

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
    for project in projects:
        if project.total_target > 0:
            project.progress_percentage = round((project.current_amount / project.total_target) * 100, 2)
        else:
            project.progress_percentage = 0  # To avoid division by zero
    return render(request, 'Project/project_list.html', {'projects': projects})


@login_required
def project_details(request, pk):
    project = get_object_or_404(Project, id=pk)
    similar_projects = Project.objects.filter(tags__in=project.tags.all()).exclude(pk=pk).distinct()[:4]
    is_reported = project.is_reported  # Check if the project is reported
    report_count = project.reports.count()
    
    ratings = Rating.objects.filter(project=project)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']

    # Fetch comments related to the project
    comments = Comment.objects.filter(project=project)  

    # Check if the current user has reported the project
    user_has_reported = False
    if request.user.is_authenticated:
        user_has_reported = project.reports.filter(user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            user = CustomUser.objects.get(pk=request.user.pk)
            comment = comment_form.save(commit=False)
            comment.user = user
            comment.project = project
            comment.save()
            return redirect('project_details', pk=pk)
    else:
        comment_form = CommentForm()

    rating_form = RatingForm()
    report_comment_form = ReportCommentForm()
    return render(request, 'Project/project_details.html', {
        'project': project,
        'similar_projects': similar_projects,
        'comment_form': comment_form,
        'is_reported': is_reported,
        'report_count': report_count,
        'comments': comments,  # Include comments in the context
        'report_comment_form': report_comment_form,
        'rating_form': rating_form,
        'average_rating': average_rating,
        'user_has_reported': user_has_reported,  # Pass the user_has_reported variable to the template
    })

@login_required
def report_project(request, pk):
    project = get_object_or_404(Project, id=pk)
    user = request.user.customuser  # Fetch the CustomUser instance

    # Check if the user has already reported this project
    existing_report = Report.objects.filter(user=user, project=project).exists()
    if existing_report:
        # Redirect with a message or handle as per your requirements
        return redirect('project_details', pk=project.id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            
            # Create a new report instance
            report = Report.objects.create(user=user, project=project, reason=reason)
            report.save()
            
            # Set project as reported (if needed)
            project.is_reported = True
            project.save()
            
            return redirect('project_details', pk=project.id)  # Redirect to project details page
    else:
        form = ReportForm()
    
    return render(request, 'Project/project_details.html', {'project': project, 'form': form})


@login_required
def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    user = CustomUser.objects.get(pk=request.user.pk)

    # Check if the user has already reported this comment
    already_reported = ReportComment.objects.filter(comment=comment, user=user).exists()
    if already_reported:
        messages.warning(request, 'You have already reported this comment.')

    if request.method == 'POST':
        form = ReportCommentForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            report_comment = ReportComment(comment=comment, user=user, reason=reason)
            report_comment.save()
            messages.success(request, 'Comment successfully reported.')
            return redirect('project_details', pk=comment.project.pk)
    else:
        form = ReportCommentForm()

    context = {'report_comment_form': form, 'already_reported': already_reported}
    return render(request, 'Project/report_comment.html', context)


# ========================================================================================================================
# CRUD operations
# ========================================================================================================================


@login_required
def create_project(request):
    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        image_form = ProjectImageForm(request.POST, request.FILES)
        tag_form = TagForm(request.POST)

        if project_form.is_valid() and tag_form.is_valid():
            project = project_form.save(commit=False)
            user_id = request.user.id
            creator = get_object_or_404(CustomUser, id=user_id)
            project.creator = creator
            project.save()

            # Save project images
            if image_form.is_valid():
                for image in request.FILES.getlist('images'):
                    image_form.clean_image()
                    ProjectImage.objects.create(project=project, image=image)

            # Save project tags
            if 'name' in tag_form.cleaned_data:
                tag_names = tag_form.cleaned_data['name']
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)

            return redirect('project_detail', project_id=project.id)
    else:
        project_form = ProjectForm()
        image_form = ProjectImageForm()
        tag_form = TagForm()

    return render(request, 'projects/create_project.html', {
        'project_form': project_form,
        'image_form': image_form,
        'tag_form': tag_form,
    })


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project_detail.html', {'project': project})


@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        image_form = UpdateProjectImageForm(request.POST, request.FILES, prefix='image')
        tag_form = UpdateTagForm(request.POST, prefix='tag')

        if project_form.is_valid() and tag_form.is_valid():
            project = project_form.save(commit=False)
            project.save()
            # Remove images if selected
            if 'remove_image' in request.POST:
                images_to_remove = request.POST.getlist('remove_image')
                for image_id in images_to_remove:
                    project.images.filter(id=image_id).delete()
                    # Remove tags if selected
            if 'remove_tag' in request.POST:
                tags_to_remove = request.POST.getlist('remove_tag')
                for tag_id in tags_to_remove:
                    project.tags.remove(int(tag_id))

            # Update project images
            if image_form.is_valid():

                # Add new images if provided
                if image_form.cleaned_data['images']:
                    for image in request.FILES.getlist('image-images'):
                        ProjectImage.objects.create(project=project, image=image)

            # Update project tags
            if tag_form.is_valid():

                # Add new tags if provided
                if tag_form.cleaned_data['name']:
                    tag_names = tag_form.cleaned_data['name']
                    for tag_name in tag_names:
                        tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                        project.tags.add(tag)

            return redirect('project_detail', project_id=project.id)
    else:
        project_form = ProjectForm(instance=project)
        image_form = UpdateProjectImageForm(prefix='image')
        tag_form = UpdateTagForm(prefix='tag')

    return render(request, 'projects/update_project.html', {
        'project_form': project_form,
        'image_form': image_form,
        'tag_form': tag_form,
        'project': project,
    })


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


# ========================================================================================================================
# CRUD operations
# ========================================================================================================================


def home(request):
    # project_images = ProjectImage.objects.all()
    # print(project_images)
    projects = Project.objects.all().order_by('-created_at')[:5]
    # print(projects)
    featured_projects = Project.objects.filter(is_featured=True)
    # featured_images = ProjectImage.objects.filter(project__is_featured=True)
    # progress = []
    # progress_featured = []
    # for project in projects:
    #     if project.total_target != 0:
    #         percent_complete = (project.current_amount / project.total_target) * 100
    #     else:
    #         percent_complete = 0  # Avoid division by zero
    #
    #     progress.append({'project_id': project.id, 'percent_complete': percent_complete})

    # for featured in featured_projects:
    #     if featured.total_target != 0:
    #         percent_complete = (featured.current_amount / featured.total_target) * 100
    #     else:
    #         percent_complete = 0
    #     progress_featured.append({'project_id': featured.id, 'percent_complete': percent_complete})

    # return render(request, 'Home/home.html', {'projects': projects, 'project_images': project_images, 'progress': progress
    #                                           , 'featured_projects': featured_projects
    #                                           , 'featured_images': featured_images
    #                                           , 'progress_featured': progress_featured})
    return render(request, 'Home/home.html', {'projects': projects, 'featured_projects': featured_projects})


def search(request):
    return render(request, 'Home/search.html')


@login_required
def donate(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = DonationForm(request.POST, initial={'project': project})
        if form.is_valid():
            try:
                form.save(project)
                return JsonResponse({'success': True})
            except forms.ValidationError as e:
                errors = {'detail': str(e)}
                return JsonResponse({'success': False, 'errors': errors})
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = DonationForm(initial={'project': project})
    return render(request, 'Project/project_list.html', {'form': form, 'project': project})


######rating as an integer input###########
# @login_required
# def rate_project(request, project_id):
#     if request.method == 'POST':
#         # Get the authenticated user

#         # Ensure user is logged in
#         if not request.user.is_authenticated:
#             return JsonResponse({'error': 'User must be logged in to rate a project.'}, status=401)

#         # Retrieve the user instance from the database using the user's primary key
#         try:
#             user = CustomUser.objects.get(pk=request.user.pk)
#         except CustomUser.DoesNotExist:
#             return JsonResponse({'error': 'User does not exist.'}, status=404)

#         # Get the project
#         project = get_object_or_404(Project, id=project_id)

#         # Get the rating value from the request
#         rating_value = int(request.POST.get('rating', 0))  # Assuming the rating is submitted via a form with name 'rating'

#         # Check if the rating value is valid (between 1 and 5)
#         if 1 <= rating_value <= 5:
#             # Create or update the rating
#             rating, _ = Rating.objects.update_or_create(user=user, project=project, defaults={'rating': rating_value})

#             # Update the project's total rating count and value
#             project.update_rating()

#             # Redirect back to the project detail page
#             return redirect('project_details', pk=project_id)
#         else:
#             # If the rating value is invalid, return a JsonResponse with an error message
#             return JsonResponse({'error': 'Invalid rating value. Rating value must be between 1 and 5.'}, status=400)

#     # Handle GET requests by redirecting to the project detail page
#     return redirect('project_details', pk=project_id)


######rating as stars input###########
@login_required
def rate_project(request, project_id):
    if request.method == 'POST':
        # Retrieve the rating value from the form
        rating_value = int(request.POST.get('rating', 0))

        # Validate rating value (optional)

        # Update the rating value in the database for the project
        project = get_object_or_404(Project, id=project_id)
        # project.rating = rating_value
        # project.save()
        # Create or update the rating
        user = CustomUser.objects.get(pk=request.user.pk)
        rating, _ = Rating.objects.update_or_create(user=user, project=project, defaults={'rating': rating_value})

        # Update the project's total rating count and value
        project.update_rating()

        # Redirect back to the project detail page
        return redirect('project_details', pk=project_id)

    # Handle GET requests if needed


def search_helper(request):
    search_query = request.GET.get('search')
    projects = Project.objects.all()

    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(tags__name__icontains=search_query) |
            Q(category__name__icontains=search_query)
        ).distinct()

    # Render the search results template with the filtered projects
    html = render(request, 'Home/search_results.html', {'projects': projects}).content.decode('utf-8')
    return JsonResponse({'html': html})

# url home
# home design

# project multiple images in latest and featured
# refactor home function and the progress bar
# picture in project details X
# project details when image is clicked X
