from typing import Iterable
from django.db import models
from authentication.models import Account
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
# Create your models here.


User = settings.AUTH_USER_MODEL


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

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categoryies")

    def __str__(self):
        return self.name

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

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        # Call the real save() method
        super(Chnnel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("Channel_detail", kwargs={"pk": self.pk})
