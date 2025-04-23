from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProjectView, ProjectByIdView, FormSubmissionView, FormSubmissionByIdView, FormFieldResponseView, FormFieldResponseByIdView, AssignSubmissionView, FormSubmissionDetailView, GetSubmissionsByFormIdView, ProjectBySubjectView

router = DefaultRouter()
# router.register(r'projects', ProjectView, basename='project')

# urlpatterns = router.urls

urlpatterns = [
    path('', ProjectView.as_view(), name='project'),
    path('<int:pk>', ProjectByIdView.as_view(), name='project_by_id'),
    path('submission', FormSubmissionView.as_view(), name='from_submission'), # Get all submit
    path('submission/<int:pk>', FormSubmissionByIdView.as_view(), name='from_submission_by_id'),
    path('submission/detail/<int:submission_id>', FormSubmissionDetailView.as_view(), name='from_submission_detail_by_id'),
    path('submission/<int:form_id>/assign', AssignSubmissionView.as_view(), name='assign_submit_form'),
    path('submission/project/<int:project_id>/form/<int:form_id>', GetSubmissionsByFormIdView.as_view(), name='get_submissions_by_project_id'),
    path('subject/<int:subject_id>', ProjectBySubjectView.as_view(), name='project_by_subject'),

    path('fieldresponse', FormFieldResponseView.as_view(), name='from_fiel_response'),
    path('fieldresponse/<int:pk>', FormFieldResponseByIdView.as_view(), name='from_fiel_response_by_id'),
]