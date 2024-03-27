from django.db import models
from authentication.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    current_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    total_rating_count = models.IntegerField(default=0)
    total_rating_value = models.IntegerField(default=0)

    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    is_reported = models.BooleanField(default=False)
    reason_for_report = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/Projects/{self.id}'

    def update_rating(self):
        ratings = Rating.objects.filter(project=self)
        self.total_rating_count = ratings.count()
        self.total_rating_value = sum(rating.rating for rating in ratings)
        self.save()

    def calculate_average_rating(self):
        if self.total_rating_count > 0:
            return self.total_rating_value / self.total_rating_count
        return 0

    def get_status(self):
        if self.is_active and self.current_amount < self.total_target:
            return "Active"
        elif not self.is_active and self.current_amount < self.total_target:
            return "Suspended"
        elif not self.is_active and self.current_amount >= self.total_target:
            return "Reached Target"
        else:
            return "Unknown"


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('user', 'project')  # Ensure each user can rate a project only once


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')

    @property
    def image_url(self):
        return f'/media/{self.image}'


class Tag(models.Model):
    name = models.CharField(max_length=50)
    projects = models.ManyToManyField(Project, related_name='tags')

    def __str__(self):
        return self.name


# ///////////////////////////////////// COMMENT MODEL//////////////////////////////////////////////////////////////////////////////////


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_reported = models.BooleanField(default=False)
    reason_for_report = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.project.title}'


class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.user.username} on {self.comment}'



class ReportComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report on comment {self.comment.id} by {self.user.username}"


# ///////////////////////////////////// COMMENT MODEL//////////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////// REPORT MODEL//////////////////////////////////////////////////////////////////////////////////

class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report on {self.project.title} by {self.user.username}"

# ///////////////////////////////////// REPORT MODEL//////////////////////////////////////////////////////////////////////////////////
