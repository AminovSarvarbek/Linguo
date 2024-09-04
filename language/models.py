from django.db import models


class Language(models.Model):
    language = models.CharField(max_length=10)
    short_name = models.CharField(max_length=4, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.language