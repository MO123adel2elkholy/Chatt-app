from django.contrib import admin
from .models import (
    Server, Chnnel, Category
)
# Register your models here.

admin.site.register((
    Server, Chnnel, Category,
))
