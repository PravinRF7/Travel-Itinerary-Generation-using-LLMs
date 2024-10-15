from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blog'  # Make sure the app name matches in your URLs

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.Login, name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('verify/', views.verify, name='verify'),
    path('demo/', views.demo, name='demo'),
    path('amristar/', views.amristar_view, name='amristar'),
    path('agra/', views.agra_view, name='agra'),
    path('goa/', views.goa_view, name='goa'),
    path('pondicherry/', views.pondicherry_view, name='pondicherry'),
    path('kullu/', views.kullu_view, name='kullu'),
    path('andamanislands/', views.andamanislands_view, name='andamanislands'),
    path('saveenquiry/', views.save_enquiry, name='saveenquiry'),
    path('search/', views.search_view, name='search'),
    path('search-results/', views.search_results, name='search_results'),
    path('get-weather/', views.get_weather, name='get_weather'),
    path('generate-itinerary/', views.generate_itinerary, name='generate_itinerary'),
    path('result/', views.result, name='result'),
    path('travel_details/', views.travel_details, name='travel_details'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
