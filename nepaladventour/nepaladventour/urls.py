from django.contrib import admin
from django.urls import path
from login.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/',home, name="home"),
    path('',home),
    path('signin/', signin, name='signin'),
    path('signout/',signout),
    path('signup/', signup, name='signup'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('navBar/', navBar, name='navBar'),
    path('footer/', footer),
    path('users/',user_view, name='user_view'),
    path('hotels/',hotels, name="hotels"),
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
    path('search_results/',search_results, name="search_results"),
    path('activity_view/',activity_view, name="activity_view"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
