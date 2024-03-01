from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path(
        route='password_reset/<uidb64>/<token>/',
        view=views.password_reset,
        name='password_reset'
    ),
    path('change-password/', views.change_password, name='change_password'),
    path('edit_account/', views.edit_account, name='edit_account'),
]
