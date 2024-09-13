from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_views
from .forms import Cust_User_CreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = Cust_User_CreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) #Authomatically log in the user
            return redirect('Profile')
        else:
            form = Cust_User_CreationForm()
            return render(request, 'blog/register.html', {'form': form})
        
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})