from django.conf import settings
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Category(models.Model):
    category = models.CharField(max_length=60)

    def __str__(self):
        return self.category



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('blogfuncional.Category', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images', blank=True)
    article_description = models.TextField(max_length=500, default='Читать далее')
    title = models.CharField(max_length=200)
    text = RichTextUploadingField()
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blogfuncional.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve_comment(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

