from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password
from login.models import *  
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# Home Page
def home(request):
    if request.user.is_authenticated:
        return render(request, "userss/home.html")
    else:
        return redirect('/signin')


@login_required
def user_profile(request):
    return render(request, 'userss/user_profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    # Assuming 'profile' is an extension of the Django user, related by a OneToOneField to the Django User model
    user_profile = request.user  # Access the user's profile directly since profile is an AbstractUser extension

    if request.method == 'POST':
        fullname = request.POST.get('fullname', user_profile.fullname)
        username = request.POST.get('username', user_profile.username)
        connect = request.POST.get('connect', user_profile.connect)
        social_media = request.POST.get('social_media', user_profile.social_media)

        # For profile picture, because it's a file, we handle it a bit differently
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile.profile_picture = profile_picture

        # Now assign the other fields
        user_profile.fullname = fullname
        user_profile.username = username
        user_profile.connect = connect
        user_profile.social_media = social_media

        # Finally, save the updated profile
        user_profile.save()

        # Redirect to a new URL: this could be the profile page where the user can see their updated profile
        messages.success(request, 'Your profile was successfully updated.')
        return HttpResponseRedirect(reverse('user_profile'))  # Make sure 'user_profile' is the name of your profile view

    # If the request method isn't POST, display the profile form with existing information
    context = {'profile': user_profile}
    return render(request, 'userss/edit_profile.html', context)

# Login Page
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Check if the user is an admin 
            if user.is_superuser or user.is_staff:
                return redirect('/admin_dashboard/') 
            else:
                # Redirect to a general user page
                return redirect('/home')  
        else:
            # If authentication fails, return an error message
            error_message = 'Authentication failed. Please check your username and password.'
            return render(request, "userss/login.html", {'error_message': error_message})
    else:
        # If not a POST request, just render the login page
        return render(request, "userss/login.html")

# Logout
def signout(request):
    logout(request)
    return redirect('/signin')

# Signup Page
def signup(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        profile_picture = request.FILES.get('profile_picture')
        connect = request.POST.get('connect')
        social_media = request.POST.get('social_media')

        # Check if the username already exists before creating a new user
        if profile.objects.filter(username=username).exists():
            return render(request, 'userss/signup.html', {'error_message': 'Username already exists'})
        elif password != confirmpassword:
            return render(request, 'userss/signup.html', {'error_message': 'Passwords do not match'})
        else:
            #Creating User
            user = profile.objects.create_user(username=username, password=password, email=email, fullname=fullname, connect=connect, social_media=social_media)

            # Handling profile_picture separately because it's a file field
            if profile_picture:
                user.profile_picture = profile_picture

            user.save()

            return redirect('/signin')
    else:
        return render(request, "userss/signup.html")

# Admin Dashboard
def admin_dashboard(request):
    profiles = profile.objects.all()
    return render(request, "admin/admin_dashboard.html", {'profiles': profiles})

#Admins
def admin_view(request):
    profiles = profile.objects.filter(is_superuser=True)
    paginator = Paginator(profiles, 5)  # Show 5 profiles per page

    page = request.GET.get('page')
    profiles = paginator.get_page(page)
    return render(request, "admin/admins/admin_view.html",{'profiles': profiles})

def add_admin(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        profile_picture = request.FILES.get('profile_picture')
        connect = request.POST.get('connect')
        social_media = request.POST.get('social_media')

        # Check if the username already exists before creating a new user
        if profile.objects.filter(username=username).exists():
            return render(request, 'admin/admins/add_user.html', {'error_message': 'Admin Username already exists'})
        elif password != confirmpassword:
            return render(request, 'admin/admins/add_user.html', {'error_message': 'Passwords do not match'})
        else:
            #Creating User
            user = profile.objects.create_superuser(username=username, password=password, email=email, fullname=fullname, connect=connect, social_media=social_media)

            # Handling profile_picture separately because it's a file field
            if profile_picture:
                user.profile_picture = profile_picture

            user.save()

            return redirect('admin_view')
    else:
        return render(request, "admin/admins/add_admin.html")

def edit_admin(request, id):
    # Fetch the user profile to edit based on user_id
    user_profile = get_object_or_404(profile, pk=id)

    if request.method == 'POST':
        fullname = request.POST.get('fullname', user_profile.fullname)
        username = request.POST.get('username', user_profile.username)
        connect = request.POST.get('connect', user_profile.connect)
        social_media = request.POST.get('social_media', user_profile.social_media)

        # Handle profile picture update
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile.profile_picture = profile_picture

        # Assign the updated fields
        user_profile.fullname = fullname
        user_profile.username = username
        user_profile.connect = connect
        user_profile.social_media = social_media

        # Save the updated profile
        user_profile.save()

        messages.success(request, 'User profile successfully updated.')
        return HttpResponseRedirect(reverse('admin_view'))  # Redirect to the admin view of users

    # For GET request, display the profile form with existing information
    context = {'profile': user_profile, 'user_id': id}
    return render(request, 'admin/admins/edit_admin.html', context)

def delete_admin(request, id):
    # Check if the requesting user's username is 'admin'
    if request.user.username == 'admin':
        # Prevent 'admin' from deleting their own profile
        if request.user.id == id:
            messages.error(request, "You cannot delete your own admin account.")
        else:
            user_profile = get_object_or_404(profile, id=id)
            user_profile.delete()
            messages.success(request, "User deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete users.")
    
    return redirect('admin_view')

#Admin Hotels
def hotel_view(request):
    hotels = Hotel.objects.filter()
    paginator = Paginator(hotels, 5)  # Show 5 profiles per page

    page = request.GET.get('page')
    hotels = paginator.get_page(page)
    return render(request, "admin/hotels/hotel_view.html",{'hotels': hotels})

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Hotel
from django.core.files.storage import FileSystemStorage

def add_hotel(request):
    if request.method == "POST":
        name = request.POST.get('name')
        type_of_hotel = request.POST.get('type_of_hotel')
        price = request.POST.get('price')
        budget = request.POST.get('budget')
        address = request.POST.get('address')
        city = request.POST.get('city', 'Default City')  # Using 'Default City' if city is not provided
        contact = request.POST.get('contact')
        description = request.POST.get('description')
        picture = request.FILES.get('picture')

        # Optional: Add more validations as needed, for example, checking for duplicate hotel names.

        # Create and save the new hotel instance
        new_hotel = Hotel(
            name=name,
            type_of_hotel=type_of_hotel,
            price=price,
            budget=budget,
            address=address,
            city=city,
            contact=contact,
            description=description,
            picture=picture  # Directly assign the uploaded file to the ImageField
        )
        new_hotel.save()

        # Redirect to a success page or the hotel list page
        return redirect('hotel_view')  # Ensure you have defined this URL name in your urls.py
    else:
        # If not a POST request, just render the hotel registration form page
        return render(request, "admin/hotels/add_hotel.html")  # Update the path to your hotel registration form template


#Admin Activities
def activity_view(request):
    activities = Activity.objects.filter()
    paginator = Paginator(activities, 5)  # Show 5 profiles per page

    page = request.GET.get('page')
    activities = paginator.get_page(page)
    return render(request, "admin/activities/activity_view.html",{'activities':activities})

# Navbar
def navBar(request):
    return render(request, "shared/navBar.html")

#Footer
def footer(request):
    return render(request, "shared/footer.html")

def hotels(request):
    return render(request, "userss/Hotels.html")
#Search Results
def search_results(request):
    return render(request, "userss/Search_Results.html")

#users
def user_view(request):
    profiles = profile.objects.filter(is_superuser=False)
    paginator = Paginator(profiles, 5) 

    page = request.GET.get('page')
    profiles = paginator.get_page(page)
    return render(request, "admin/users/users.html",{'profiles': profiles})


    
#update user data from the database through admin panel

def edit_user(request, id):
    # Fetch the user profile to edit based on user_id
    user_profile = get_object_or_404(profile, pk=id)

    if request.method == 'POST':
        fullname = request.POST.get('fullname', user_profile.fullname)
        username = request.POST.get('username', user_profile.username)
        connect = request.POST.get('connect', user_profile.connect)
        social_media = request.POST.get('social_media', user_profile.social_media)

        # Handle profile picture update
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            user_profile.profile_picture = profile_picture

        # Assign the updated fields
        user_profile.fullname = fullname
        user_profile.username = username
        user_profile.connect = connect
        user_profile.social_media = social_media

        # Save the updated profile
        user_profile.save()

        messages.success(request, 'User profile successfully updated.')
        return HttpResponseRedirect(reverse('user_view'))  # Redirect to the admin view of users

    # For GET request, display the profile form with existing information
    context = {'profile': user_profile, 'user_id': id}
    return render(request, 'admin/users/edit_user.html', context)

#delete user data from the database through admin panel

def delete_user(request, id):
    profiles= profile.objects.get(id=id)
    profiles.delete()
    messages.info(request, "User Deleted Successfully")
    return redirect('user_view')

from django.shortcuts import render
from .models import Hotel, Activity

def search_results(request):
    query = request.GET.get('query', '')
    hotels = Hotel.objects.filter(city__icontains=query)
    activities = Activity.objects.filter(city__icontains=query)
    address_hotels = Hotel.objects.filter(name__icontains=query, city__icontains=query)
    address_activities = Activity.objects.filter(name__icontains=query, city__icontains=query)

    context = {
        'query': query,
        'hotels': hotels,
        'activities': activities,
        'address_hotels': address_hotels,
        'address_activities': address_activities
    }

    if query:
        template_name = 'search_results.html'
    else:
        template_name = 'search_results_empty.html'

    return render(request, template_name, context)
