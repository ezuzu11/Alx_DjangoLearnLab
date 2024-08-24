from django.shortcuts import render, redirect  #Redirect for registration (User Authentication)
from .models import Book
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.forms import UserCreationForm # refers to registration (User Authentication)
from django.contrib.auth import login
## Role-Based Access Control 
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

# Implementing Custom Permissions
from django.contrib.auth.decorators import permission_required
from .models import Book, Author
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
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
            user = form.save() #If the form is valid, the user is created and saved to the database.
            login(request, user)
            return redirect('home')
            #return redirect('login') #After successfully creating the user, this redirects the user to the login page.
        else:
            form = UserCreationForm() #If the request is not a POST (e.g., it's a GET request), we create a blank instance of UserCreationForm to display an empty form.
        return render(request, 'relationship_app/register.html', {'form': form}) #This renders the register.html template, passing the form instance to the template’s context.

# Role-Based Access Control 

## Admin View
def admin_check(user):
    return user.userprofile.role == 'Admin'
@user_passes_test(admin_check)
def admin_view(request):
    #return HttpResponse("Admin view accessed")
    return render(request, 'relationship_app/admin_view.html')

## Librarian View
def librarian_check(user):
    #Ensure user has a UserProfile before accessing the role
    if hasattr(user, 'userprofile'):
        return user.userprofile.role == 'Librarians'
    return False
    
@user_passes_test(librarian_check)
def librarian_view(request):
    #return HttpResponse("Librarian view accessed")
    return render(request, 'relationship_app/librarian_view.html')
## Member View
def member_check(user):
    return user.userprofile.role == 'Member'
@user_passes_test(member_check)
def member_view(request):
    #return HttpResponse("Member view accessed")
    return render(request, 'relationship_app/member_view.html')

# Implementing Custom Permissions
#Add book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        author = Author.objects.get(id=author_id)

        # Create and save the book
        book = Book.objects.create(title=title, author=author)
        return redirect('book_list')  # Assuming you have a view that lists books

    # If GET, render the form (you'll need to create an HTML form to add books)
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})

# Update book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        author_id = request.POST.get('author_id')
        book.author = get_object_or_404(Author, id=author_id)
        book.save()
        return redirect('book_list')  # Redirect to the book list view

    authors = Author.objects.all()
    return render(request, 'relationship_app/update_book.html', {'book': book, 'authors': authors})


# delete book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Redirect to the book list view

    return render(request, 'relationship_app/confirm_delete.html', {'book': book})