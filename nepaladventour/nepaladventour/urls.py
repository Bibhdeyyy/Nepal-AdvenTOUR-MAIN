from django.contrib import admin
from django.urls import path
from login.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/',home, name="home"),
    path('',home),
    
    path('navBar/', navBar, name='navBar'),
    path('footer/', footer),

    path('signin/', signin, name='signin'),
    path('signout/',signout),
    path('signup/', signup, name='signup'),

    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
   
    path('admin_view/',admin_view, name='admin_view'),

    path('user_profile/', user_profile, name='user_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    
    path('add_admin/', add_admin, name="add_admin"),
    path('edit_admin/<int:id>/', edit_admin, name="edit_admin"),
    path('delete_admin/<int:id>/', delete_admin, name="delete_admin"),

    path('user_view/',user_view,name='user_view'),
    path('edit_user/<int:id>/', edit_user, name="edit_user"),
    path('delete_user/<int:id>/', delete_user, name="delete_user"),

    path('hotel_view/',hotel_view, name="hotel_view"),
    path('add_hotel/',add_hotel, name="add_hotel"),
    path('delete_hotel/<int:id>',delete_hotel, name="delete_hotel"),
    path('edit_hotel/<int:id>/',edit_hotel, name="edit_hotel"),
    path('delete_hotel_image/<int:id>/', delete_hotel_image, name="delete_hotel_image"),

    path('hotels/',hotels, name="hotels"),
    path('search_hotels/',search_hotels, name="search_hotels"),
    path('search_hotel_results/', filter_hotels, name='search_hotel_results'),
    path('hotel_details/<int:id>/', hotel_details, name='hotel_details'),

    path('search_activity/',search_activity, name="search_activity"),
    path('activity_search_results/', activity_search_results, name='activity_search_results'),
    path('activities/',activities, name="activities"),
    path('activity_details/<int:id>/', activity_details, name='activity_details'),

    path('activity_view/',activity_view, name="activity_view"),
    path('add_activity/',add_activity, name="add_activity"),
    path('edit_activity/<int:id>/',edit_activity, name="edit_activity"),
    path('delete_activity_image/<int:id>/', delete_activity_image, name="delete_activity_image"),
    path('delete_activity/<int:id>',delete_activity, name="delete_activity"),
    
    path('hotel_review/',hotel_review, name="hotel_review"),
    path('add_hotel_review<int:id>/', add_hotel_review, name='add_hotel_review'),
    path('delete_hotel_review/<int:id>',delete_hotel_review, name="delete_hotel_review"),
    
    path('activity_review/',activity_review, name="activity_review"),
    path('delete_activity_review/<int:id>',delete_activity_review, name="delete_activity_review"),

    path('about_us/',about_us, name="about_us"),

    path('get_hotels_nearby', get_hotels_nearby, name='get_hotels_nearby'),
    
    path('add_activity_review<int:id>/', add_activity_review, name='add_activity_review'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
