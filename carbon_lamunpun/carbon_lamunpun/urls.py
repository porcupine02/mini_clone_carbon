"""
URL configuration for carbon_lamunpun project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import health_check, FormsWithSubmissionsBySubjectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls')),
    path('project/', include('project.urls')),
    path('form/', include('forms.urls')),
    path('', health_check),
    path('subject/<int:subject_id>/forms-with-submissions/', FormsWithSubmissionsBySubjectView.as_view(), name='dashboard_form_submit'),
]
