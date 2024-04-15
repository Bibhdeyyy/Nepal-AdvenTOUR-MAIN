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


def add_hotel(request):
    if request.method == "POST":
        # Collecting data from the form
        name = request.POST.get('name')
        type_of_hotel = request.POST.get('type_of_hotel')
        price = request.POST.get('price')
        budget = request.POST.get('budget')
        address = request.POST.get('address')
        city = request.POST.get('city')
        contact = request.POST.get('contact')
        description = request.POST.get('description')
        main_picture = request.FILES.get('picture')  # This fetches the main hotel picture

        # Creating and saving the new Hotel instance with the main picture
        new_hotel = Hotel(
            name=name,
            type_of_hotel=type_of_hotel,
            price=price,
            budget=budget,
            address=address,
            city=city,
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
        age_required = request.POST.get('age_required')
        price = request.POST.get('price')
        address = request.POST.get('address')
        city = request.POST.get('city')
        contact = request.POST.get('contact')
        status = request.POST.get('status')
        main_picture = request.FILES.get('picture')
        
        activity = Activity(
            name=name,
            age_required=age_required,
            price=price,
            address=address,
            city=city,
            contact=contact,
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

def delete_activity_review(request, id):
    activity_reviews = ActivityReview.objects.get(id=id)
    activity_reviews.delete()
    messages.success(request, "Activity Reviews deleted successfully.")
    return redirect('activity_review')


# Navbar
def navBar(request):
    return render(request, "shared/navBar.html")

#Footer
def footer(request):
    return render(request, "shared/footer.html")

def hotels(request):
    return render(request, "userss/Hotels.html")




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
    # This will fetch distinct activity names ordered by name
    activities = Activity.objects.order_by('name').values_list('name', flat=True).distinct()
    return render(request, 'userss/search_activity.html', {
        'activities': activities
    })

def activity_search_results(request):
    # Get the activity name from the GET request
    activity_name = request.GET.get('activity_name', '')

    # Filter activities based on the selected name
    activities = Activity.objects.filter(name=activity_name) if activity_name else Activity.objects.none()

    # Render a template with the filtered activities
    return render(request, 'userss/activity_search_results.html', {'activities': activities})

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