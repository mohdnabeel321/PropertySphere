from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Property 
from .forms import PropertyForm

# Home Page View (Shows login/signup links before login, and properties after login)
def home(request):
    if request.user.is_authenticated:
        # If the user is logged in, redirect to the logged-in home page
        return redirect('home_logged_in')
    else:
        # If the user is not logged in, show login/signup options and allow exploring properties
        properties = Property.objects.all()  # Optional: Show properties even when not logged in
        return render(request, 'home_logged_out.html', {'properties': properties})

# Home Page for Logged-In Users
def home_logged_in(request):
    # Render home page for logged-in users showing properties
    properties = Property.objects.all()
    return render(request, 'home_logged_in.html', {'properties': properties})

def home_logged_out(request):
    # This is the page shown for logged-out users
    properties = Property.objects.all()  # Optional: Show properties even when not logged in
    return render(request, 'home_logged_out.html', {'properties': properties})

# Property List Page (Only accessible after login)
@login_required
def property_list(request):
    # Display all properties added by the user or globally
    properties = Property.objects.filter(user=request.user) 
    return render(request, 'property_list.html', {'properties': properties})

# Add Property (For logged-in users to add properties)
@login_required
def add_property(request):    
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.user = request.user  # Assign the current logged-in user to the property
            property_instance.save()
            return redirect('property_list')  # Redirect to the property list or wherever
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form': form})
# Property Detail Page (Allows users to view details of the property)
def property_detail(request, pk):
    property = Property.objects.get(pk=pk)
    return render(request, 'property_detail.html', {'property': property})

# Sign Up View
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=form.cleaned_data.get('password1'))
            login(request, user)
            return redirect('home_logged_in')  # Redirect to property list after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_logged_in')  # Redirect to property list after login
        else:
            # You could also show an error message here
            return redirect('login')  # Invalid login credentials, retry
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home_logged_out')  # Redirect to home after logging out


# Edit Property View
@login_required
def edit_property(request, pk):
    # Get the property object; ensure it's the logged-in user's property
    property = get_object_or_404(Property, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_list')  # Redirect to the property list or wherever
    else:
        form = PropertyForm(instance=property)  # Pre-fill the form with the current data
    
    return render(request, 'edit_property.html', {'form': form, 'property': property})

# Delete Property View
@login_required
def delete_property(request, pk):
    # Get the property object; ensure it's the logged-in user's property
    property = get_object_or_404(Property, pk=pk, user=request.user)
    
    if request.method == 'POST':
        property.delete()  # Delete the property
        return redirect('property_list')  # Redirect to the property list or wherever

    return render(request, 'confirm_delete.html', {'property': property})
