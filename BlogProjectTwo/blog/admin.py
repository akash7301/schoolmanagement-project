from django.contrib import admin
from .models import Post,Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','auther','body','publish','created','updated','status']
    prepopulated_fields = {'slug':('title',)}
    list_filter = ('status','auther','created','publish',)
    search_fields = ('title','body',)
    raw_id_fields = ('auther',)
    date_hierarchy = 'publish'
    ordering = ['status','publish']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','post','created','updated','active']
    list_filter = ('active','created','updated',)
    search_fields = ('name','email','body',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment,CommentAdmin)
