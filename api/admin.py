from django.contrib import admin
from api.models import User, Profile, Category, Post

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Post)