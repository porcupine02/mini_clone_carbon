from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import FormsView, FormsByIdView, FormFieldsView, FormFieldsByIdView, SubjectView, SubjectByIdView, CreateFormAndFormFields, LinkFormToSubjectView, FormsBySubjectView, AddMainFormByIdView, FormsSubjectView, MainFormBySubjectView
# from .views import FormsView, FormsByIdView, FormFieldsView, FormFieldsByIdView, SubjectView, SubjectByIdView, CreateFormAndFormFields, LinkFormToSubjectView, FormsBySubjectView, AddMainFormByIdView, FormsSubjectView, FormsSubjectBySubjIdView, MainFormBySubjectView

router = DefaultRouter()

urlpatterns = [
    path('', FormsView.as_view(), name='form'),
    path('<int:pk>', FormsByIdView.as_view(), name='form_by_id'),
    path('field', FormFieldsView.as_view(), name='from_field'),
    path('field/<int:pk>', FormFieldsByIdView.as_view(), name='from_field_by_id'),
    path('subject', SubjectView.as_view(), name='subject_response'),
    path('subject/<int:pk>', SubjectByIdView.as_view(), name='subject_by_id'),
    path('subject/<int:subject_id>/all-forms', FormsBySubjectView.as_view(), name='get_form_by_subject'), # Get Form by subject

    path('with-fields', CreateFormAndFormFields.as_view(), name='form_with_fields'),
    # add update and delete


    path('subject/<int:subject_id>/add-forms', LinkFormToSubjectView.as_view(), name='link_form_subject'),
    path('add-main/<int:pk>', AddMainFormByIdView.as_view(), name='set_main_form_subject'),
    path('link-form-subject', FormsSubjectView.as_view(), name='form_subject'),
    # path('link-form-subject/<int:pk>', FormsSubjectBySubjIdView.as_view(), name='form_detail_subject_submit'),
    path('main-forms/<int:subject_id>/', MainFormBySubjectView.as_view(), name='main_forms_by_subject'),


]