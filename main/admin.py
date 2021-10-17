from django.contrib import admin

# Register your models here.
from .models import Customer,Comment,Post

admin.site.register(Customer)
admin.site.register(Post)
admin.site.register(Comment)
