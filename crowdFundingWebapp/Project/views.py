from django import forms
from .forms import CategoryForm, DonationForm, ProjectForm, ProjectImageForm, TagForm, CommentForm, ReportForm, \
    ReportCommentForm, \
    UpdateProjectImageForm, UpdateTagForm, RatingForm,ReplyForm
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Project, ProjectImage, Tag, Report, Comment, ReportComment, Rating, Reply
from django.contrib.auth.decorators import login_required
from authentication.models import CustomUser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Avg, Q
from django.contrib import messages
from django.contrib.auth import get_user_model,logout
from authentication.views import admin_login


# Create your views here.

@login_required
def create_category(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
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
    except Exception as e:
        return render(request, 'admin/admin_errors.html', {'error_message': str(e)})

    return render(request, 'admin/create_category.html', {'categories': categories, 'form': form})

@login_required
def categoryDetails(request, category_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            category = get_object_or_404(Category, pk=category_id)
            projects = category.project_set.all()           
            featured_projects_count = projects.filter(is_featured=True).count()
            active_projects_count = 0
            suspended_projects_count = 0
            completed_projects_count = 0
            for project in projects:
                if project.total_target > 0:
                    project.progress_percentage = round((project.current_amount / project.total_target) * 100, 2)
                else:
                    project.progress_percentage = 0
                status = project.get_status()
                if status == "Active":
                    active_projects_count += 1
                elif status == "Suspended":
                    suspended_projects_count += 1
                elif status == "Reached Target":
                    completed_projects_count += 1
            average_rating = projects.aggregate(avg_rating=Avg('rating__rating'))['avg_rating'] or 0
            return render(request, 'admin/category_details.html', {
                'category': category,
                'projects': projects,
                'featured_projects_count': featured_projects_count,
                'active_projects_count': active_projects_count,
                'suspended_projects_count': suspended_projects_count,
                'reached_target_projects_count': completed_projects_count,
                'average_rating': average_rating
            })
    except Exception as e:
        return render(request, 'admin/admin_errors.html', {'error_message': str(e)})
    
@login_required
def select_featured_projects(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            projects = Project.objects.all()
            for project in projects:
                if project.total_target > 0:
                    project.progress_percentage = round((project.current_amount / project.total_target) * 100, 2)
                else:
                    project.progress_percentage = 0
            return render(request, 'admin/featured_project.html', {'projects': projects })
    except Exception as e:
        return render(request, 'admin/admin_errors.html', {'error_message': str(e)})


@csrf_exempt
def update_featured_status(request, project_id):
    try:
        if request.method == 'POST':
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
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@login_required
def report_details_admin(request,project_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:

            project = get_object_or_404(Project, id=project_id)
            reports = project.reports.all()
            tags = project.tags.all()
            return render(request, 'admin/admin_report_details.html', {'project': project, 'reports': reports , 'tags':tags})
    except Exception as e:
        return render(request, 'admin/admin_errors.html', {'error_message': str(e)})

@login_required
def admin_suspend_project(request, project_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            project = get_object_or_404(Project, id=project_id)
            if request.method == 'POST':
                project.is_active = False
                project.save()
                return redirect('admin_home')
            return render(request, 'admin/suspend_project_confirmation.html', {'project': project})
    except Exception as e:
        return render(request, 'admin/admin_errors.html', {'error_message': str(e)})

@login_required
def admin_delete_project(request, project_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            project = get_object_or_404(Project, id=project_id)
            if request.method == 'POST':
                project.delete()
                return redirect('admin_home')
            return render(request, 'admin/delete_project_confirmation.html', {'project': project})
    except Exception as e:
        return render(request, 'admin/admin_errors.html', {'error_message': str(e)})

@login_required
def admin_ignore_reports(request, project_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            project = get_object_or_404(Project, id=project_id)
            report = get_object_or_404(Report, project_id=project_id)

            if request.method == 'POST':
                if project.current_amount < project.total_target:
                    project.is_active = True
                project.is_reported = False
                report.delete()
                project.save()
                return redirect('admin_home')
            return render(request, 'admin/ignore_reports_confirmation.html', {'project': project})
    except Exception as e:
        return render(request, 'admin/admin_errors.html', {'error_message': str(e)})

@login_required
def admin_project_details(request,project_id):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            project = get_object_or_404(Project, id=project_id)
            reports = project.reports.all()
            tags = project.tags.all()
            ratings = Rating.objects.filter(project=project)
            average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            return render(request, 'admin/admin_project_details.html',
                        {'project': project, 'reports': reports , 'tags':tags, 'average_rating': average_rating,'noOfRating': project.total_rating_count,})
    except Exception as e:
        return render(request, 'admin/admin_errors.html', {'error_message': str(e)})

@login_required
def admin_logout(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            logout(request)
            return redirect(admin_login)
    except Exception as e:
        return render(request, 'admin/admin_errors.html', {'error_message': str(e)})
    

def error_page(request):
    error_message = 'An error occurred.'
    return render(request, 'Project/error_page.html', {'error_message': error_message})



def project_list(request):
    try:
        projects = Project.objects.all()
        for project in projects:
            if project.total_target > 0:
                project.progress_percentage = round((project.current_amount / project.total_target) * 100, 2)
            else:
                project.progress_percentage = 0  # To avoid division by zero
        return render(request, 'Project/project_list.html', {'projects': projects})
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'Error retrieving projects.'})



def project_details(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'Project not found.'})

    similar_projects = Project.objects.filter(tags__in=project.tags.all()).exclude(pk=pk).distinct()[:4]
    is_reported = project.is_reported  # Check if the project is reported
    report_count = project.reports.count()
    
    ratings = Rating.objects.filter(project=project)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    # Fetch the user's rating for the project, if exists
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, project=project).first()

    # Fetch comments related to the project
    try:
        comments = Comment.objects.filter(project=project)
    except ObjectDoesNotExist:
        comments = []

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
        'noOfRating': project.total_rating_count,
        'user_rating': user_rating,
        'user_has_reported': user_has_reported,  # Pass the user_has_reported variable to the template
    })



@login_required
def report_project(request, pk):
    try:
        project = Project.objects.get(id=pk)
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'Project not found.'})

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


@login_required
def reply_comment(request, parent_id):
    
    try:
        parent_comment = Comment.objects.get(pk=parent_id)
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'Comment not found.'})

    project = parent_comment.project  # Get the project related to the parent comment

    if request.method == 'POST':
        form = ReplyForm(request.POST)  # Using the correct form
        if form.is_valid():
            reply_text = form.cleaned_data['text']
            user = request.user.customuser   # Get the user object from the request
            if isinstance(user, get_user_model()):  # Check if the user object is an instance of CustomUser
                # Create a new Reply object but don't save it yet
                reply_comment = Reply(comment=parent_comment, user=user, text=reply_text)
                # Save the reply_comment object to the database
                reply_comment.save()
                messages.success(request, 'Reply added successfully.')
                return redirect('project_details', pk=project.pk)  # Redirect to project details page
            else:
                messages.error(request, 'Error creating reply. Please try again.')
        else:
            messages.error(request, 'Error creating reply. Please try again.')
    else:
        messages.error(request, 'Invalid request method.')

    # Redirect to project details page in case of GET request or form validation errors
    return redirect('project_details', pk=project.pk)



# ========================================================================================================================
# CRUD operations
# ========================================================================================================================



@login_required
def create_project(request):
    if request.method == 'POST':
        try:
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
                        ProjectImage.objects.create(project=project, image=image)

                # Save project tags
                if 'name' in tag_form.cleaned_data:
                    tag_names = tag_form.cleaned_data['name']
                    for tag_name in tag_names:

                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        project.tags.add(tag)

                return redirect('project_detail', project_id=project.id)
        except Exception as e:
            print(f"An error occurred: {e}")
            # Redirect to an error page or display a message to the user
            return render(request, 'projects/error.html', context={'error_message': str(e)})
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
    try:
        project = get_object_or_404(Project, id=project_id)
    except Exception as e:
        # Handle the case where the project does not exist
        return render(request, 'projects/error.html', context={'error_message': str(e)})

    # Calculate progress percentage and format to 2 decimal places
    if project.total_target > 0:
        progress_percentage = round((project.current_amount / project.total_target) * 100, 2)
    else:
        progress_percentage = 0  # To avoid division by zero

    return render(request, 'projects/project_detail.html', {'project': project, 'progress_percentage': progress_percentage})


@login_required
def update_project(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
    except ObjectDoesNotExist:
        return render(request, 'projects/error.html', context={'error_message': 'Project does not exist.'})

    if request.method == 'POST':
        try:
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
        except Exception as e:
            return render(request, 'projects/error.html', context={'error_message': str(e)})
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
    try:
        project = get_object_or_404(Project, id=project_id, creator=request.user)
    except ObjectDoesNotExist:
        # Handle the case where the project does not exist
        return render(request, 'projects/error.html', context={'error_message': 'Project does not exist.'})

    # Check if the donated amount exceeds 25% of the total target
    if (project.current_amount / project.total_target) * 100 > 25:
        return render(request, 'projects/error.html', context={'error_message': 'Donated amount exceeds 25% of total target. Deletion not allowed.'})

    if request.method == 'POST':
        try:
            project.delete()
        except Exception as e:
            # Handle the case where an unexpected error occurs
            return render(request, 'projects/error.html', context={'error_message': str(e)})
        return redirect('user_projects')
    return render(request, 'projects/delete_project.html', {'project': project})

@login_required
def user_projects(request):
    try:
        projects = Project.objects.filter(creator=request.user)
    except Exception as e:
        # Handle the case where an unexpected error occurs
        return render(request, 'projects/error.html', context={'error_message': str(e)})
    return render(request, 'projects/user_projects.html', {'projects': projects})
# ========================================================================================================================
# CRUD operations
# ========================================================================================================================


def home(request):
    try:
        projects = Project.objects.all().filter(is_active=True).order_by('-created_at')[:5]
        featured_projects = Project.objects.filter(is_featured=True , is_active=True)
        rated_projects = []
        for project in Project.objects.all():
            average_rating = project.calculate_average_rating()
            rated_projects.append((project, average_rating))

        highest_rated_projects = sorted(rated_projects, key=lambda x: x[1], reverse=True)[:5]
        # highest_rated_projects = [project for project, _ in highest_rated_projects]

        print(highest_rated_projects)
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'Error retrieving projects.'})
    return render(request, 'Home/home.html', {'projects': projects, 'featured_projects': featured_projects
                                              , 'highest_rated_projects': highest_rated_projects})


def search(request):
    return render(request, 'Home/search.html')


@login_required
def donate(request, pk):
    try:
        project = Project.objects.get(pk=pk)
        if request.method == 'POST':
            form = DonationForm(request.POST, initial={'project': project})
            if form.is_valid():
                try:
                    form.save(project)
                    success_message = f'Thank you for your donation of ${form.cleaned_data["donation_amount"]}.'
                    if project.is_featured :
                        project.is_featured = 0
                        project.save()
                    return JsonResponse({'success': True, 'success_message': success_message})
                except forms.ValidationError as e:
                    errors = {'detail': str(e)}
                    return JsonResponse({'success': False, 'errors': errors})
            else:
                errors = form.errors
                return JsonResponse({'success': False, 'errors': errors})
        else:
            form = DonationForm(initial={'project': project})
        return render(request, 'Project/project_list.html', {'form': form, 'project': project})
    except Project.DoesNotExist:
        return JsonResponse({'success': False, 'errors': {'detail': 'Project does not exist'}})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': {'detail': str(e)}})


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
    try:
        if request.method == 'POST':
            print("hello")
            # Retrieve the rating value from the form
            rating_value = int(request.POST.get('rating', 0))

            # Validate rating value (optional)

            # Update the rating value in the database for the project
            project = get_object_or_404(Project, id=project_id)
            # project.rating = rating_value
            # project.save()
            # Create or update the rating
            user = CustomUser.objects.get(pk=request.user.pk)
            # Check if the user has previously rated the project
            rating, created = Rating.objects.get_or_create(user=user, project=project)
            rating.rating = rating_value
            rating.save()

                # Update the project's total rating count and value
            project.update_rating()

            # Redirect back to the project detail page
            return redirect('project_details', pk=project_id)

        # Handle GET requests if needed
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'Error in Rating process.'})



def search_helper(request):
    try:
        search_query = request.GET.get('search')
        projects = Project.objects.all()

        if search_query:
            projects = projects.filter(
                Q(title__icontains=search_query) |
                Q(tags__name__icontains=search_query) |
                Q(category__name__icontains=search_query)
            ).distinct()
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'Error retrieving projects.'})

    # Render the search results template with the filtered projects
    html = render(request, 'Home/search_results.html',
                  {'projects': projects, 'search_query': search_query}).content.decode('utf-8')
    return JsonResponse({'html': html})


def all_categories(request):
    try:
        categories = Category.objects.all().values('id', 'name')
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'Error retrieving categories.'})
    return JsonResponse(list(categories), safe=False)


def category_projects(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        projects = Project.objects.filter(category=category)
    except ObjectDoesNotExist:
        return render(request, 'Project/error_page.html', {'error_message': 'Category not found.'})
    return render(request, 'category/category_projects.html', {'projects': projects,'category':category})


def custom_404_view(request, exception):
    return render(request, 'Project/error_page.html', {'error_message': 'Url not found'},status=404)