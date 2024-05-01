from string import whitespace
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
import os
from PIL import Image


def upload_location(instance, filename):
    file_path = 'blog/user_{author_id}/{slug}_post.jpeg'.format(
        author_id=str(instance.author.id), slug=str(instance.slug), filename=filename
    )
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(full_path):
        os.remove(full_path)
    return file_path


class Category(MPTTModel):
    category_name = models.CharField(max_length=50, null=True, default='others', blank=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="category_parent")
    date_updated = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name_plural = "categories"


    def __str__(self):
        return self.category_name

    class MPTTMeta:        
        order_insertion_by = ['date_updated']

    def __str__(self):
        full_path = [self.category_name]
        p = self.parent
        while p is not None:
            full_path.append(p.category_name)
            p = p.parent
        return ' -> '.join(full_path[::-1])


class BlogPost(models.Model):
    title = models.CharField(max_length=250, null=False, blank=False)
    category = models.ManyToManyField(Category, verbose_name='categories', default=1)
    body = RichTextUploadingField(null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author")
    slug = models.SlugField(blank=True, unique=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    @property
    def image_url(self):
        try:
            image = self.image.url
        except :
            image =""
        return image
    
    def get_absolute_url(self):
        return reverse('blog:details', args=[self.slug])

    class Meta:
        ordering = (
            '-date_published',
        )

    def __str__(self):
        return self.title


@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


@receiver(post_save, sender=BlogPost)
def save_img(sender, instance, *args, **kwargs):
    SIZE = 600, 600
    if instance.image:
        pic = Image.open(instance.image.path)
        try:
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(instance.image.path)
        except:
            if pic.mode in ("RGBA", 'P'):
                blog_pic = pic.convert("RGB")
                blog_pic.thumbnail(SIZE, Image.LANCZOS)
                blog_pic.save(instance.image.path)        


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)


# comment
class Comment(MPTTModel):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="comment_parent")
    name_comment = models.CharField(max_length=50)
    email_comment = models.EmailField(null=True)
    username_comment = models.CharField(max_length=50, null=True)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ("-date_published",)

    def __str__(self):
        return f"Comment by {self.name_comment}"
