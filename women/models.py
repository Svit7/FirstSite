from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models import Q
from mptt.models import MPTTModel, TreeForeignKey
from .middleware import get_current_user


class Women(models.Model):
    name = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Post text")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Photo")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Create data")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Upload data")
    is_published = models.BooleanField(default=False, verbose_name="Publication")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Category")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                               verbose_name='Author', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = "Famous women"
        verbose_name_plural = "Famous women"
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Category")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['id']


class Contact(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                               verbose_name='Contact author', on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Create data")
    name = models.CharField(max_length=255, db_index=True, verbose_name="Name")
    email = models.EmailField(verbose_name='Email')
    content = models.TextField(blank=True, verbose_name="Contact")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contact"
        ordering = ['id']


class StatusFilterComments(models.Manager):
    """
    Prevents non-author of the comment from viewing comments with status=False
    """
    def get_queryset(self):
        user = get_current_user()
        if user is not None and not user.is_authenticated:
            return super().get_queryset().filter(status=True).select_related('author')
        return super().get_queryset().filter(Q(status=False, author=get_current_user()) |
                                             Q(status=False, post__author=get_current_user()) |
                                             Q(status=True)).select_related('author')


class Comments(MPTTModel):
    post = models.ForeignKey(Women, blank=True, null=True, related_name='comments_post',
                             verbose_name='Post', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                               verbose_name='Comment author', on_delete=models.CASCADE)
    text = models.TextField(blank=True, verbose_name='Comment')
    status = models.BooleanField(default=False, verbose_name='Article Visibility')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Create data')
    objects = StatusFilterComments()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    class MPTTMeta:
        order_insertion_by = ['id']
