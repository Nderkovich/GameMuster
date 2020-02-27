from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


app_name = 'user_profile'


urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('<int:profile_id>/', views.profile_view, name='profile'),
    path('activate/uid=<str:uidb64>/token=<str:token>/', views.activation_view, name='activation'),
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('logout/', views.logout_view, name='logout')
]
