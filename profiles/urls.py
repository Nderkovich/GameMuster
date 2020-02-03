from django.urls import path
from . import views


app_name = 'user_profile'


urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('profile/<int:id>', views.profile_view, name='profile'),
    path('activate/uid=<str:uidb64>/token=<str:token>/', views.activation_view, name='activation'),
    path('add_to_favorite/<int:game_id>/', views.add_to_favorites_view, name='add_to_favorite'),
    path('remove_from_favorite/<int:game_id>/', views.remove_from_favorites_view, name='remove_from_favorite')
]
