from django.db import models
from ckeditor.fields import RichTextField
from language.models import Language


class Course(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = RichTextField()

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title