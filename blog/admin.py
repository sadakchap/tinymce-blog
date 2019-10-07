from django.contrib import admin
from .models import Author,Comment,Post
# Register your models here.

admin.site.register(Author)

class CommntInline(admin.StackedInline):
	model 	= Comment
	extra	= 3

class PostAdmin(admin.ModelAdmin):
	list_display		= ['title','author','created','updated','feature']
	prepopulated_fields = {'slug':('title',)}
	inlines = [
        CommntInline,
    ]

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
