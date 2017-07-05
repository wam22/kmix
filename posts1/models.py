from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .utils import get_read_time, unique_slug_generator

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        qs = self.get_queryset().filter(
                            draft=False,
                            publish__lte=timezone.now()
                            )
        return qs


def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(unique=True, blank=True)
    image           = models.ImageField(upload_to=upload_location, 
                        null=True, 
                        blank=True, 
                        width_field="width_field", 
                        height_field="height_field")
    likes           = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    height_field    = models.IntegerField(default=0)
    width_field     = models.IntegerField(default=0)
    content         = models.TextField()
    updated         = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp       = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects         = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})


    # def get_api_url(self):
    #     return reverse("posts-api:detail", kwargs={"slug": self.slug})

    
    class Meta:
        ordering = ["-timestamp", "-updated"]

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    if instance.content:
        read_time_var = get_read_time(instance.content)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Post)
