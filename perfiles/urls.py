from perfiles.views import login_view, CustomLogoutView
from django.urls import path

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', CustomLogoutView.as_view(), name="logout")
]