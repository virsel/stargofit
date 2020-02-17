"""
Definition of urls for all_nice_fourth.
"""

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.member_login, name='login'),
    path('logout/', views.member_logout, name='logout'),
    path('register/', views.register, name='register'),
    #path('logout/',views.LogoutView.as_view(), name = 'logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('dashboard/profile/', views.ProfileView, name='profile'),
    path('dashboard/settings/', views.ProfileSettingsView, name='profile_settings'),
    path('dashboard/member_plans/', views.ProfilePlansView, name='member_plans'),
    path('dashboard/member_favorites/', views.ProfileFavoritesView,
         name='member_favorites'),
]
