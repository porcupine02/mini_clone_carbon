from django.urls import path
from .views import LogoutView, RegisterView, LoginView, TeacherView, RoleListView, TestView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('teachers/', TeacherView.as_view(), name='test'),
    path('roles/', RoleListView.as_view(), name='role'),
    path('test/', TestView.as_view(), name='test'),
]
