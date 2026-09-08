from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models.CategoriesModel import Category
from .models.PostModel import Post
from .models.SectionModel import Section
from .models.TagModel import Tag
from .models.PageModel import Page
from .models.ContactUsModel import ContactUs
from .models.UsersModel import Users
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

# Categories
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }

    list_display = ['title', 'slug', 'status', 'created_at', 'updated_at']
    list_filter = ['title', 'status']
    exclude = ['created_at', 'updated_at']


admin.site.register(Category, CategoriesAdmin)


# Sections
class SectionsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }

    list_display = ['title', 'slug', 'status', 'created_at', 'updated_at']
    list_filter = ['title', 'status']
    exclude = ['created_at', 'updated_at']


admin.site.register(Section, SectionsAdmin)


# Tags
class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }

    list_display = ['title', 'slug', 'status', 'created_at', 'updated_at']
    list_filter = ['title', 'status']
    exclude = ['created_at', 'updated_at']


admin.site.register(Tag, TagsAdmin)


# Posts
class PostsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }

    list_display = ['title', 'slug', 'status', 'section', 'created_at', 'updated_at']
    list_filter = ['title', 'status', 'section']
    exclude = ['created_at', 'updated_at', 'view_numbers']


admin.site.register(Post, PostsAdmin)


# Page
class PageAdmin(admin.ModelAdmin):
    # readonly_fields = ['slug']
    prepopulated_fields = {
        'slug': ['title']
    }

    list_display = ['title', 'slug', 'status', 'created_at', 'updated_at']
    list_filter = ['title', 'slug', 'status']
    exclude = ['created_at', 'updated_at']


admin.site.register(Page, PageAdmin)


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['status']
    exclude = ['created_at', 'updated_at', 'token_id']


admin.site.register(ContactUs, ContactUsAdmin)


class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_superuser', 'is_active', 'date_joined']
    exclude = ['email_active_code']


admin.site.register(Users, UsersAdmin)