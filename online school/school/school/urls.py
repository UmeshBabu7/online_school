"""
URL configuration for school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from app_school.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_data, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout'),
    path('instructor/', instructor, name='instructor'),
    path('add_course/', add_course, name='add_course'),
    path('all_course/', view_all_course, name='all_course'),
    path('view_course/<int:course_id>/', view_course, name='view_course'),
    path('add_blog/', add_blog, name='add_blog'),
    path('all_blog/', view_all_blog, name='all_blog'),
    path('blog/<int:key>', blog, name='blog'),
    path('add_review/', add_review, name='add_review'),
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('enroll/<int:course_id>/payment/', payment_process, name='payment_process'),
    path('enroll/payment/success/', payment_success, name='payment_success'),
    path('contact/', contact_form, name='contact_form'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
