from django.db import models
from authentication.models import CustomUser


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

    total_rating = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)

    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


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


class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.project.title}'