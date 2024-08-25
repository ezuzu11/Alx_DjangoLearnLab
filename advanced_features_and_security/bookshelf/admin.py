from django.contrib import admin
from .models import Book
# Customer User Model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title', 'author', 'publication_year')
    search_fields= ('title', 'author')
    list_filter= ('publication_year',)

# Customer User Model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)