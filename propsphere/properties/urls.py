from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Home page (will redirect to the property list if logged in)
    path('home_logged_in/', views.home_logged_in, name='home_logged_in'),
    path('home_logged_out/', views.home_logged_out, name='home_logged_out'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('add-property/', views.add_property, name='add_property'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('property-list/', views.property_list, name='property_list'),
    path('property/<int:pk>/edit/', views.edit_property, name='edit_property'),
    path('property/<int:pk>/delete/', views.delete_property, name='delete_property'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
