from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(profile)
admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(HotelReview)
admin.site.register(Activity)
admin.site.register(ActivityImage)
admin.site.register(ActivityReview)
admin.site.register(Recommendation)