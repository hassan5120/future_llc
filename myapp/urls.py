from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('our_team', views.team, name='team'),
    path('services', views.services, name='services'),
    path('specialities', views.specialities, name='specialities'),
    path('softwares', views.softwares, name='softwares'),
    path('testimonials', views.testimonials, name='testimonials'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('send_email', views.send_email, name='send_email'),
    path('submit_review', views.submit_review, name='submit_review'),
    path('register', views.register, name='register'),
    path('loginuser', views.loginuser, name='loginuser'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
