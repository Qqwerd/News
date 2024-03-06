from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'dateCreation']
    list_filter = ('author', 'dateCreation', 'rating')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['postThrough', 'categoryThrough']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['commentPost', 'commentUser', 'dateCreation', 'rating']
    list_filter = ('commentUser', 'dateCreation', 'rating')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['authorUser', 'ratingAuthor']
    list_filter = ('authorUser', 'ratingAuthor')



admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)