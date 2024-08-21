from django.shortcuts import render, redirect  #Redirect for registration (User Authentication)
from .models import Book
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.forms import UserCreationForm # refers to registration (User Authentication)
from django.contrib.auth import login
# Create your views here.

#Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view for displaying library details
class LibraryDetailView(DetailView):
    model = Library  # Specify the model
    template_name = 'relationship_app/library_detail.html'  # Template to use
    context_object_name = 'library'  # Context variable name

# Function to Register a User
def register(request):
    if request.method == 'POST': #In web forms, POST requests are typically used to submit data (like a registration form).
        form = UserCreationForm(request.POST) #If the request is a POST, we create an instance of UserCreationForm with the data submitted by the user (request.POST).
        if form.is_valid():
            form.save() #If the form is valid, the user is created and saved to the database.
            return redirect('login') #After successfully creating the user, this redirects the user to the login page.
        else:
            form = UserCreationForm() #If the request is not a POST (e.g., it's a GET request), we create a blank instance of UserCreationForm to display an empty form.
        return render(request, 'relationship_app/register.html', {'form': form}) #This renders the register.html template, passing the form instance to the template’s context.
    