
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('oauth2callback/', admin.site.urls),
    path('api/', include('books.urls')),
]
