from django.contrib import admin
from .models import Post, Puntuer, Comment
# Register your models here.

class PuntuerAdmin(admin.ModelAdmin):
    pass


class ComentAdmin(admin.ModelAdmin):
    pass


class PostAdmi(admin.ModelAdmin):
    pass

admin.site.register(Puntuer)
admin.site.register(Comment)
admin.site.register(Post)
