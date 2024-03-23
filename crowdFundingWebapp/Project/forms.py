from django import forms
from .models import Category, Project, Tag, Comment
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from .models import Project, ProjectImage, Tag


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 4:
            raise forms.ValidationError("Name must be at least 4 characters long.")
        return name


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


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['creator', 'current_amount', 'total_rating', 'rating_count', 'is_active', 'is_featured']
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
    class Meta:
        model = ProjectImage
        fields = ['image']
        # widgets = {'image': forms.FileInput(attrs={'multiple': True})}


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        # widgets = {'image': forms.FileInput(attrs={'multiple': True})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
        
class ReportForm(forms.Form):
    reason = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter reason for reporting'}))