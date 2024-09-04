from django.db import models
from ckeditor.fields import RichTextField


class Blog(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)
    content = RichTextField()

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title