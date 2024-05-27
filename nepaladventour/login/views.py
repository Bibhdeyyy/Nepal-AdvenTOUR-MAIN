# Importing Libraries
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
from django.http import HttpResponseNotAllowed
from django.db.models import Avg
from django.db.models import Count
from datetime import timedelta
from django.utils.timezone import now
from datetime import date
import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from math import radians, sin, cos, sqrt, atan2
from .recommendations import recommend_hotels_item_based
from .activity_recommendations import recommend_activities_content_based, recommend_activities_item_based
import math
from django.http import HttpResponseServerError

# Home Page
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('/admin_dashboard/')
        else:
            top_hotels = Hotel.objects.order_by('-rating')[:10]
            return render(request, "userss/home.html", {'top_hotels': top_hotels})
    else:
        return redirect('/signin')


@login_required
def user_profile(request):
    return render(request, 'userss/user_profile.html', {'user': request.user})

#User edit profile
@login_required
def edit_profile(request):
    user_profile = request.user  # Access the user's profile

    if request.method == 'POST':
        fullname = request.POST.get('fullname', user_profile.fullname)
        username = request.POST.get('username', user_profile.username)
        connect = request.POST.get('connect', user_profile.connect)
        social_media = request.POST.get('social_media', user_profile.social_media)

        #Handling Profile Picture
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
        
        # Attempt to authenticate the user with the provided credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser or user.is_staff:
                return redirect('/admin_dashboard/') 
            else:
                return redirect('/home')  
        else:
            # Authentication failed, set an error message
            error_message = 'Authentication failed. Please check your username and password.'

            return render(request, "userss/login.html", {'error_message': error_message})
    else:
        return render(request, "userss/login.html")

# Logout
def signout(request):
    logout(request)
    return redirect('/signin')

# Signup Page
def signup(request):
    # Check if the incoming request is a POST request
    if request.method == "POST":
        # Extracting user d etails from the POST request
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        profile_picture = request.FILES.get('profile_picture')  # Handling file upload
        connect = request.POST.get('connect')
        social_media = request.POST.get('social_media')

        # Verify if the username is already taken
        if profile.objects.filter(username=username).exists():
            return render(request, 'userss/signup.html', {'error_message': 'Username already exists'})
        
        elif password != confirmpassword:
            return render(request, 'userss/signup.html', {'error_message': 'Passwords do not match'})
        
        else:
            # Create a new user if validations pass
            user = profile.objects.create_user(username=username, password=password, email=email, 
                                               fullname=fullname, connect=connect, social_media=social_media)

            # Save the profile picture if provided
            if profile_picture:
                user.profile_picture = profile_picture

            # Save user details to the database
            user.save()

            # Redirect user to sign-in page after successful registration
            return redirect('/signin')
    else:
        # Show the signup form if not a POST request
        return render(request, "userss/signup.html")


# Admin Dashboard
def admin_dashboard(request):
    if request.user.is_authenticated:
        # Count the number of admins and users
        admin_count = profile.objects.filter(is_staff=True).count()
        user_count = profile.objects.filter(is_staff=False).count()

        # Count the number of hotels with each rating
        hotel_ratings = Hotel.objects.values('rating').annotate(count=Count('rating')).order_by('rating')
        ratings = [str(hotel['rating']) for hotel in hotel_ratings]  # Convert ratings to string for JSON compatibility
        hotel_counts = [hotel['count'] for hotel in hotel_ratings]

        # Count the number of activities with each rating
        activity_ratings = Activity.objects.values('rating').annotate(count=Count('rating')).order_by('rating')
        activity_labels = [str(activity['rating']) for activity in activity_ratings]  # Convert ratings to string for JSON compatibility
        activity_counts = [activity['count'] for activity in activity_ratings]

        # Get the average rating of activities by type
        activity_data = Activity.objects.values('type').annotate(avg_rating=Avg('rating')).order_by('type')
        activity_types = [activity['type'] for activity in activity_data]
        avg_ratings = [float(activity['avg_rating']) for activity in activity_data]

        # Data for the Bar Chart
        data = [admin_count, user_count]
        labels = ["Admins", "Users"]

        context = {
            'data': data,
            'labels': labels,
            'ratings': ratings,
            'hotel_counts': hotel_counts,
            'activity_labels': activity_labels,
            'activity_counts': activity_counts,
            'activity_types': json.dumps(activity_types),
            'avg_ratings': json.dumps(avg_ratings),
        }

        return render(request, "admin/admin_dashboard.html", context)
    else:
        return render(request, "userss/login.html")


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
            user = profile.objects.create_superuser(username=username, password=password, email=email,
                                                     fullname=fullname, connect=connect, social_media=social_media)

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
        messages.error(request, "You are not authorized to delete admins.")
    
    return redirect('admin_view')

#Admin Hotels
def hotel_view(request):
    hotels = Hotel.objects.filter()
    paginator = Paginator(hotels, 5)  # Show 5 profiles per page

    page = request.GET.get('page')
    hotels = paginator.get_page(page)
    return render(request, "admin/hotels/hotel_view.html",{'hotels': hotels})

def hotels(request):
    # Fetch all hotel records from the database
    hotels = Hotel.objects.all()

    # Render the template, passing the 'hotels' context variable
    return render(request, 'userss/hotels.html', {'hotels': hotels})

@login_required
def add_hotel_review(request, id):
    hotel = get_object_or_404(Hotel, pk=id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        description = request.POST.get('description')
        HotelReview.objects.create(
            hotel=hotel,
            user=request.user,  # Automatically capture the logged-in user's profile
            rating=rating,
            description=description,
        )
        # Redirect to the hotel detail page, or wherever is appropriate
        return redirect('hotel_details', id=hotel.id)

    # If GET, show the empty form -- though this can be skipped if form is POST only
    return render(request, 'userss/add_hotel_review.html', {'hotel': hotel})

def add_hotel(request):
    if request.method == "POST":
        # Collecting data from the form
        name = request.POST.get('name')
        type_of_hotel = request.POST.get('type_of_hotel')
        price = request.POST.get('price')
        budget = request.POST.get('budget')
        rating = request.POST.get('rating')
        address = request.POST.get('address')
        city = request.POST.get('city')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        contact = request.POST.get('contact')
        description = request.POST.get('description')
        main_picture = request.FILES.get('picture')  # This fetches the main hotel picture

        # Creating and saving the new Hotel instance with the main picture
        new_hotel = Hotel(
            name=name,
            type_of_hotel=type_of_hotel,
            price=price,
            budget=budget,
            rating=rating,
            address=address,
            city=city,
            longitude = longitude,
            latitude = latitude,
            contact=contact,
            description=description,
            picture=main_picture  # Assign the main picture here
        )
        new_hotel.save()
        
        # Handling the upload of additional images
        additional_images = request.FILES.getlist('images')  # Fetches all files selected for the 'images' input
        for image in additional_images:
            # For each image, create a new HotelImage instance linked to the newly created Hotel
            HotelImage.objects.create(hotel=new_hotel, image=image)
        
        # Redirect to a success or detail view of the hotel after the hotel and its images have been saved
        return redirect('hotel_view')  # Make sure 'hotel_view' is the correct URL name for your success or detail view
    else:
        # Render the hotel registration form for GET requests
        return render(request, "admin/hotels/add_hotel.html")

#Hotel Edit
def edit_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    
    if request.method == "POST":
        # Update hotel fields with form data
        hotel.name = request.POST.get('name', hotel.name)
        hotel.type_of_hotel = request.POST.get('type_of_hotel', hotel.type_of_hotel)
        hotel.price = request.POST.get('price', hotel.price)
        hotel.budget = request.POST.get('budget', hotel.budget)
        hotel.address = request.POST.get('address', hotel.address)
        hotel.city = request.POST.get('city', hotel.city)
        hotel.longitude = request.POST.get('longitude', hotel.longitude)
        hotel.latitude = request.POST.get('latitude', hotel.latitude)
        hotel.contact = request.POST.get('contact', hotel.contact)
        hotel.description = request.POST.get('description', hotel.description)
        
        # Handling the main picture change (if a new picture is uploaded)
        new_main_picture = request.FILES.get('picture')
        if new_main_picture:
            hotel.picture = new_main_picture
        
        hotel.save()
        
        # Handling new additional images upload
        new_images = request.FILES.getlist('new_images')
        for image in new_images:
            HotelImage.objects.create(hotel=hotel, image=image)
        
        messages.success(request, "Hotel updated successfully.") 
        # Redirect to the hotel's detail view after saving changes
        return redirect('hotel_view')
    else:
        # If the request is not POST, display the form with hotel info
        return render(request, "admin/hotels/edit_hotel.html", {'hotel': hotel})

#delete Hotel
def delete_hotel(request, id):
    hotels= Hotel.objects.get(id=id)
    hotels.delete()
    messages.info(request, "Hotel Removed Successfully")
    return redirect('hotel_view')


#Delete hotel image
@require_POST
def delete_hotel_image(request, id):
    image = get_object_or_404(HotelImage, id=id)
    hotel_id = image.hotel.id
    image.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect('edit_hotel', id=hotel_id)

#Admin Activities
def activity_view(request):
    activities = Activity.objects.filter()
    paginator = Paginator(activities, 5)  # Show 5 profiles per page

    page = request.GET.get('page')
    activities = paginator.get_page(page)
    return render(request, "admin/activities/activity_view.html",{'activities':activities})

def add_activity(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')
        age_required = request.POST.get('age_required')
        price = request.POST.get('price')
        address = request.POST.get('address')
        city = request.POST.get('city')
        contact = request.POST.get('contact')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        rating = request.POST.get('rating')
        status = request.POST.get('status')
        main_picture = request.FILES.get('picture')
        
        activity = Activity(
            name=name,
            type=type,
            age_required=age_required,
            price=price,
            address=address,
            city=city,
            contact=contact,
            latitude=latitude,
            longitude=longitude,
            rating=rating,
            status=status,
            picture=main_picture
        )
        activity.save()
        
        images = request.FILES.getlist('images')
        for image in images:
            ActivityImage.objects.create(activity=activity, image=image)
            
        messages.success(request, 'New activity added successfully!')
        return redirect('activity_view')  # Assuming you have a URL pattern named 'activity_view'
    else:
        return render(request, 'admin/activities/add_activity.html')

def edit_activity(request, id):
    activity = get_object_or_404(Activity, id=id)
    
    if request.method == "POST":
        # Update activity fields with form data
        activity.name = request.POST.get('name', activity.name)
        activity.age_required = request.POST.get('age_required', activity.age_required)
        activity.price = request.POST.get('price', activity.price)
        activity.address = request.POST.get('address', activity.address)
        activity.city = request.POST.get('city', activity.city)
        activity.contact = request.POST.get('contact', activity.contact)
        activity.status = request.POST.get('status', activity.status)
        
        # Handling the main picture change (if a new picture is uploaded)
        new_main_picture = request.FILES.get('picture')
        if new_main_picture:
            activity.picture = new_main_picture
        
        activity.save()
        
        # Handling new additional images upload
        new_images = request.FILES.getlist('new_images')
        for image in new_images:
            ActivityImage.objects.create(activity=activity, image=image)
        
        messages.success(request, 'Activity updated successfully.')
        return redirect('activity_view')
    else:
        # If the request is not POST, display the form with activity info
        return render(request, "admin/activities/edit_activity.html", {'activity': activity})

def delete_activity(request, id):
    activity = Activity.objects.get(id=id)
    activity.delete()
    messages.success(request, "Activity deleted successfully.")
    return redirect('activity_view')

@require_POST
def delete_activity_image(request, id):
    image = get_object_or_404(ActivityImage, id=id)
    activity_id = image.activity.id
    image.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect('edit_activity', id=activity_id)

#Admin view Hotel Review
def hotel_review(request):
    hotel_reviews = HotelReview.objects.all()  # Retrieve all hotel reviews
    
    paginator = Paginator(hotel_reviews, 5)  # Show 5 hotel reviews per page

    page_number = request.GET.get('page')
    hotel_reviews = paginator.get_page(page_number)

    return render(request, "admin/hotel_reviews/hotel_review.html", {'hotel_reviews': hotel_reviews})

#Admin Delet Review
def delete_hotel_review(request, id):
    hotel_reviews = HotelReview.objects.get(id=id)
    hotel_reviews.delete()
    messages.success(request, "Hotel Reviews deleted successfully.")
    return redirect('hotel_review')

def activity_review(request):
    activity_reviews = ActivityReview.objects.all()  # Retrieve all hotel reviews
    
    paginator = Paginator(activity_reviews, 5)  # Show 5 hotel reviews per page

    page_number = request.GET.get('page')
    activity_reviews = paginator.get_page(page_number)

    return render(request, "admin/activity_reviews/activity_review.html", {'activity_reviews':activity_reviews})

@login_required
def add_activity_review(request, id):
    activity = get_object_or_404(Activity, pk=id)  # Ensure the activity exists
    if request.method == 'POST':
        rating = request.POST.get('rating')  # Capture the rating from the form
        description = request.POST.get('description')  # Capture the review description from the form
        ActivityReview.objects.create(
            activity=activity,
            user=request.user,  # Automatically capture the logged-in user's profile
            rating=rating,
            description=description,
        )
        # Redirect to the activity detail page, or wherever is appropriate
        return redirect('activity_details', id=activity.id)

    # If GET, show the empty form -- though this can be skipped if form is POST only
    return render(request, 'userss/add_activity_review.html', {'activity': activity})


def delete_activity_review(request, id):
    activity_reviews = ActivityReview.objects.get(id=id)
    activity_reviews.delete()
    messages.success(request, "Activity Reviews deleted successfully.")
    return redirect('activity_review')


def activity_details(request, id):
    activity = get_object_or_404(Activity, pk=id)
    reviews = ActivityReview.objects.filter(activity=activity)

    # Retrieve all activities from the database
    all_activities = Activity.objects.all()

    # Call recommend_activities_item_based function to get recommendations
    recommended_activities_df = recommend_activities_item_based(activity.name, all_activities, top_n=5)

    recommendations = []
    if not recommended_activities_df.empty:
        recommendations = recommended_activities_df.to_dict(orient='records')

    context = {
        'activity': activity,
        'recommendations': recommendations,
        'reviews': reviews, 
        'latitude': activity.latitude,
        'longitude': activity.longitude
    }
    return render(request, 'userss/activity_details_page.html', context)






# Navbar
def navBar(request):
    return render(request, "shared/navBar.html")

#Footer
def footer(request):
    return render(request, "shared/footer.html")

def about_us(request):
    return render(request, "userss/about_us.html")


def hotel_details(request, id):
    hotel = get_object_or_404(Hotel, pk=id)
    reviews = HotelReview.objects.filter(hotel=hotel)

    # Recommend hotels based on the selected hotel's name
    recommended_hotels_df = recommend_hotels_item_based(hotel.name, top_n=5)

    recommendations = []
    if not recommended_hotels_df.empty:
        # Calculate rounded distance
        recommended_hotels_df['rounded_distance'] = recommended_hotels_df['distance'].apply(lambda x: round(x))
        recommendations = recommended_hotels_df.to_dict(orient='records')

    context = {
        'hotel': hotel,
        'recommendations': recommendations,
        'reviews': reviews, 
        'latitude': hotel.latitude,
        'longitude': hotel.longitude
    }
    return render(request, 'userss/hotel_details_page.html', context)



def search_hotels(request):
    # Get distinct city values
    cities = Hotel.objects.order_by('city').values_list('city', flat=True).distinct()
    
    # Get distinct types of hotels
    types_of_hotels = Hotel.objects.order_by('type_of_hotel').values_list('type_of_hotel', flat=True).distinct()
    
    # Get distinct budgets
    budgets = Hotel.objects.order_by('budget').values_list('budget', flat=True).distinct()

    return render(request, 'userss/search_hotels.html', {
        'cities': cities,
        'types_of_hotels': types_of_hotels,
        'budgets': budgets
    })

def filter_hotels(request):
    # Fetch parameters from GET request
    city = request.GET.get('city', '')
    type_of_hotel = request.GET.get('type_of_hotel', '')
    budget = request.GET.get('budget', '')

    # Initialize empty lists to store results for each category
    hotels_by_city = []
    hotels_by_type = []
    hotels_by_budget = []
    all_criteria = []

    # Base query to modify based on inputs
    base_query = Hotel.objects.all()

    # Conditional application of filters
    if city or type_of_hotel or budget:
        if city:
            hotels_by_city = base_query.filter(city__iexact=city)
        if type_of_hotel:
            hotels_by_type = base_query.filter(type_of_hotel__iexact=type_of_hotel)
        if budget and budget.isdigit():
            hotels_by_budget = base_query.filter(budget__lte=budget)

        # Query for all criteria
        if city and type_of_hotel and budget:
            all_criteria = base_query.filter(city__iexact=city, type_of_hotel__iexact=type_of_hotel, budget__lte=budget)
            # Remove these hotels from individual lists
            hotels_by_city = [hotel for hotel in hotels_by_city if hotel not in all_criteria]
            hotels_by_type = [hotel for hotel in hotels_by_type if hotel not in all_criteria]
            hotels_by_budget = [hotel for hotel in hotels_by_budget if hotel not in all_criteria]

    # Render results to a new template
    return render(request, 'userss/hotel_search_results.html', {
        'all_criteria': all_criteria,
        'hotels_by_city': hotels_by_city,
        'hotels_by_type': hotels_by_type,
        'hotels_by_budget': hotels_by_budget,
    })

def search_activity(request):
    activities = Activity.objects.order_by('type').values_list('type', flat=True).distinct()
    return render(request, 'userss/search_activity.html', {
        'activities': activities
    })

def activity_search_results(request):
    activity_type = request.GET.get('activity_type')
    range_km = float(request.GET.get('range'))
    latitude = float(request.GET.get('latitude'))
    longitude = float(request.GET.get('longitude'))

    if activity_type:
        activities = Activity.objects.filter(type=activity_type)
    else:
        activities = Activity.objects.all()

    nearby_activities = []

    for activity in activities:
        activity_lat = activity.latitude
        activity_lon = activity.longitude

        distance = haversine_distance(latitude, longitude, activity_lat, activity_lon)
        if distance <= range_km:
            nearby_activities.append((activity, distance))

    return render(request, 'userss/activity_search_results.html', {'activities': nearby_activities})


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


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



def activities(request):
    # Annotate each activity with its average rating
    activities = Activity.objects.annotate(
        average_rating=Avg('activityreview__rating')  # Assuming 'activityreview' is the related_name
    )
    
    return render(request, 'userss/activities.html', {'activities': activities})

