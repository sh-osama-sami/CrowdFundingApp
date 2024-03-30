from django import forms
from .models import Category, Project, Tag, Comment, Reply
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, ValidationError
from django.utils import timezone
from .models import Project, ProjectImage, Tag, Rating


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 4:
            raise forms.ValidationError("Name must be at least 4 characters long.")
        return name

class DonationForm(forms.Form):
    donation_amount = forms.DecimalField(label='Donation Amount', min_value=0)
    
    def clean_donation_amount(self):
        donation_amount = self.cleaned_data['donation_amount']
        if donation_amount <= 0:
            raise forms.ValidationError("Donation amount must be greater than zero.")
        return donation_amount
    
    def save(self, project):  
        cleaned_data = self.cleaned_data
        donation_amount = cleaned_data.get('donation_amount')
        if project:
            if project.current_amount is None:
                project.current_amount = 0
            if project.current_amount + donation_amount < project.total_target:
                project.current_amount += donation_amount
                project.is_active = 1
                project.save() 
                self.success_message = f'Thank you for your donation of ${donation_amount}.'
            elif project.current_amount + donation_amount == project.total_target:
                project.current_amount += donation_amount
                project.is_active = 0
                project.save() 
            else:
                raise forms.ValidationError('Sorry, the donation amount exceeds the project total target. Please enter a smaller amount.')
        else:
            raise forms.ValidationError('Invalid donation amount. Please enter a valid amount.')

# class ProjectForm(forms.ModelForm):
#     images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
#     tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
#     class Meta:
#         model = Project
#         fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time']
#
#     # Custom validation for title field
#     title = forms.CharField(max_length=100, validators=[
#         RegexValidator(
#             regex=r'^[a-zA-Z0-9\s]+$',
#             message="Title must contain only letters, numbers, and spaces.",
#             code='invalid_title'
#         )
#     ])
#
#     # Custom validation for total_target field
#     def clean_total_target(self):
#         total_target = self.cleaned_data.get('total_target')
#         if total_target <= 0:
#             raise forms.ValidationError("Total target amount must be greater than zero.")
#         return total_target
#
#     # Custom validation for end_time field
#     def clean_end_time(self):
#         end_time = self.cleaned_data.get('end_time')
#         start_time = self.cleaned_data.get('start_time')
#         if end_time <= start_time:
#             raise forms.ValidationError("End time must be after start time.")
#         if end_time <= timezone.now():
#             raise forms.ValidationError("End time cannot be in the past.")
#         return end_time
#


# ========================================================================================================================
# CRUD operations
# ========================================================================================================================
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # Custom validation for total_target field
    def clean_total_target(self):
        total_target = self.cleaned_data.get('total_target')
        if total_target <= 0:
            raise forms.ValidationError("Total target amount must be greater than zero.")
        return total_target

    # Custom validation for end_time field
    def clean_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        start_time = self.cleaned_data.get('start_time')
        if end_time <= start_time:
            raise forms.ValidationError("End time must be after start time.")
        if end_time <= timezone.now():
            raise forms.ValidationError("End time cannot be in the past.")
        return end_time


class ProjectImageForm(forms.ModelForm):
    images = MultipleFileField(label='Select images', required=True)

    class Meta:
        model = ProjectImage
        fields = ['images']

    def clean_images(self):
        images = self.cleaned_data.get('images')
        print(images)
        for image in images:
            print("image", image)
            if not image.content_type.startswith('image'):
                print("image 2", image)
                raise ValidationError("File must be an image.")
        return images



#

class TagForm(forms.ModelForm):
    name = forms.CharField(label='Tags', required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter tags separated by commas', 'maxlength': '200'}))

    class Meta:
        model = Tag
        fields = ['name']

    def clean_name(self):
        data = self.cleaned_data.get('name')
        tags = [tag.strip() for tag in data.split(',') if tag.strip()]

        if len(tags) != len(set(tags)):
            raise ValidationError('Duplicate tags are not allowed.')

        return tags

    def clean_tag_amount(self):
        data = self.cleaned_data.get('name')
        tags = [tag.strip() for tag in data.split(',') if tag.strip()]

        # Check if the number of tags exceeds a certain limit
        max_tags_limit = 5
        if len(tags) > max_tags_limit:
            raise ValidationError(f"Maximum {max_tags_limit} tags allowed.")

        return tags

class UpdateProjectImageForm(forms.ModelForm):
    images = MultipleFileField(label='Select files', required=False)

    class Meta:
        model = ProjectImage
        fields = ['images']

    def clean_images(self):
        images = self.cleaned_data.get('images')
        for image in images:
            if not image.content_type.startswith('image'):
                raise ValidationError("File must be an image.")
        return images



class UpdateTagForm(forms.ModelForm):
    name = forms.CharField(label='Tags', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter tags separated by commas', 'maxlength': '200'}))

    class Meta:
        model = Tag
        fields = ['name']

    def clean_name(self):
        data = self.cleaned_data.get('name')
        tags = [tag.strip() for tag in data.split(',') if tag.strip()]

        # Check for duplicate tags in the current form
        if len(tags) != len(set(tags)):
            raise ValidationError('Duplicate tags are not allowed.')

        # Check for duplicate tags with existing tags in the database


        return tags

    def clean_tag_amount(self):
        data = self.cleaned_data.get('name')
        tags = [tag.strip() for tag in data.split(',') if tag.strip()]

        # Check if the number of tags exceeds a certain limit
        max_tags_limit = 5
        if len(tags) > max_tags_limit:
            raise ValidationError(f"Maximum {max_tags_limit} tags allowed.")

        return tags


# ========================================================================================================================
# CRUD operations
# ========================================================================================================================


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
  
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']

        
class ReportCommentForm(forms.Form):
    reason = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter reason for reporting'}))
    
            
class ReportForm(forms.Form):
    reason = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter reason for reporting'}))


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
