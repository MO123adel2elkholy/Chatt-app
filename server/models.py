from typing import Iterable
from django.db import models
from authentication.models import Account
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
# Create your models here.


User = settings.AUTH_USER_MODEL


def category_icon_upload_path(instance, filename):
    return f'category/{instance.id}/category_icon/{filename}'


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Category Name '),
        help_text=_('format : required , max-100'),

    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name=_('Category Description '),
        help_text=_('format : required '),

    )
    icon = models.FileField(
        upload_to=category_icon_upload_path,
        blank=True,
        null=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categoryies")

    def __str__(self):
        return self.name
#  replacing old icon with new one

    def save(self, *args, **kwargs):
        if self.id:
            exsisting = get_object_or_404(Category, id=self.id)
            if exsisting.icon != self.icon:
                exsisting.icon.delete(save=False)
        super(Category, self).save(*args, **kwargs)
    """ make sure if we deleted the category we delete images assoxiated with it 
    
    Keyword arguments: 
    argument -- description
    Return: deleted 
    """

    @receiver(models.signals.pre_delete, sender='server.Category')
    def category_delete_files(sender, instance,  **kwargs):
        for filed in instance._meta.fields:
            if filed.name == 'icon':
                file = getattr(instance, filed.name)
                if file:
                    file.delete(save=False)

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Server(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Server Name '),
        help_text=_('format : required , max-100'),

    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='servers')

    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, related_name='category_servers')
    description = models.TextField(
        blank=True, null=True,
        verbose_name=_('Server Description '),
        help_text=_('format : required '),

    )
    members = models.ManyToManyField(User)

    class Meta:
        verbose_name = _("server")
        verbose_name_plural = _("servers")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Server_detail", kwargs={"pk": self.pk})


def channel_icon_upload_path(instance, filename):
    return f'server/{instance.id}/channel_icon/{filename}'


def channel_banner_upload_path(instance, filename):
    return f'server/{instance.id}/channle_banner/{filename}'


class Chnnel(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Channel Name '),
        help_text=_('format : required , max-100'),

    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='Channel_owner')

    topic = models.CharField(
        max_length=100,
        verbose_name=_('Channel Topic '),
        help_text=_('format : required , max-100'),
    )
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name='channels')
    """
    icon = models.ImageField(
        upload_to=channel_icon_upload_path,
        blank=True,
        null=True)
    banner = models.ImageField(
        upload_to=channel_banner_upload_path,
        blank=True,
        null=True)
    """

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")

    def __str__(self):
        return self.name

        #  replacing old icon with new one
    """
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        if self.id:
            exsisting = get_object_or_404(Chnnel, id=self.id)
            if exsisting.icon != self.icon:
                exsisting.icon.delete(save=False)
            if  exsisting.banner != self.banner:
                exsisting.banner.delete(save=False)
        super(Category, self).save(*args, **kwargs)
     make sure if we deleted the chnnel  we delete images assoxiated with it 
    
    Keyword arguments: 
    argument -- description
    Return: deleted 
    
    @receiver(models.signals.pre_delete, sender='server.Server')
    def chnnels_delete_files(sender, instance,  **kwargs):
        for filed in instance._meta.fields:
            if filed.name == 'icon' or filed.name =='banner':
                file = getattr(instance, filed.name)
                if file:
                    file.delete(save=False)

    def get_absolute_url(self):
        return reverse("Channel_detail", kwargs={"pk": self.pk})
    """
