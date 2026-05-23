
from django.urls import path
from accounts.views import Register_view,CurrentUserView

urlpatterns = [
    path('registration/',Register_view.as_view()),
    path("me/", CurrentUserView.as_view()),
]