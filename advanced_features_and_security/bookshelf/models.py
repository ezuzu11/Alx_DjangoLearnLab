from django.db import models
# Custom User Model
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Book(models.Model):
    title= models.CharField(max_length=200)
    author= models.CharField(max_length=100)
    publication_year= models.IntegerField()

    def __str__(self):
        return self.title

# Custom User Model
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.username
"""
    # Implementing Custom Permissions
    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ] 
"""

    
