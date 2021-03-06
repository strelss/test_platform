from .views import *
from django.urls import path

app_name = 'login'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('newquiz/', NewQuiz, name='newquiz'),
    path('newquizadd/', newQuizAdd, name='newquizadd'),
    path('edit/<int:post_id>', edit, name='edit')
]