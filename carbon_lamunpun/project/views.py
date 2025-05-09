from django.db import IntegrityError
from .models import Project, FormSubmission, FormFieldResponse
from forms.models import Forms, FormFields
from .serializers import AssignmentsForTeacher, ProjectSerializer, FormSubmissionSerializer, FormFieldResponseSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProjectView(ListCreateAPIView):
    """ 
        ProjectView : Get/Post List (ALL) 
        Args : -
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

# Use by id
class ProjectByIdView(RetrieveUpdateDestroyAPIView):
    """ 
        ProjectByIdView : Get By Id (Single item) 
        Args : id
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

# ----------------------------------------------------- #
class FormSubmissionView(ListCreateAPIView):
    """ 
        FormSubmissionView : Get/Post List (ALL) 
        Args : -
    """
    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    permission_classes = [IsAuthenticated]


class FormSubmissionByIdView(RetrieveUpdateDestroyAPIView):
    """ 
        FormSubmissionByIdView : Get/Post/Patch/Delete By Id (Single item) 
        Args : id
    """
    queryset = FormSubmission.objects.all()
    serializer_class = FormSubmissionSerializer
    permission_classes = [IsAuthenticated]


# ----------------------------------------------------- #
class FormFieldResponseView(ListCreateAPIView):
    """ 
        FormFieldResponseView : Get/Post List (ALL) 
        Args : -
    """
    queryset = FormFieldResponse.objects.all()
    serializer_class = FormFieldResponseSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser) # TODO


class FormFieldResponseByIdView(RetrieveUpdateDestroyAPIView):
    """ 
        FormFieldResponseByIdView : Get/Post/Patch/Delete By Id (Single item) 
        Args : id
    """
    queryset = FormFieldResponse.objects.all()
    serializer_class = FormFieldResponseSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser) # TODO

class AssignSubmissionView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, form_id):
        try:
            form = Forms.objects.get(pk=form_id)
        except Forms.DoesNotExist:
            return Response({"detail": "Form not found."}, status=status.HTTP_404_NOT_FOUND)

        project_id = request.data.get("project_id")
        if not project_id:
            return Response({"detail": "Project ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({"detail": "Project not found."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        
        # Manually check if a FormSubmission exists, and update or create it.
        submission = FormSubmission.objects.filter(form=form, project=project).first()
        
        if submission:
            # If a submission already exists, update it
            submission.updated_by = user
            submission.save()
            created = False  # It's an update, not a creation
        else:
            # If no submission exists, create a new one
            submission = FormSubmission.objects.create(
                form=form,
                project=project,
                created_by=user,
                updated_by=user
            )
            created = True  # It's a creation, not an update

        fields_response_data = []
        i = 0
        while f'fieldsResponse[{i}][form_field]' in request.data:
            form_field_id = request.data.get(f'fieldsResponse[{i}][form_field]')
            value = request.data.get(f'fieldsResponse[{i}][value]')
            file = request.FILES.get(f'fieldsResponse[{i}][file]')

            fields_response_data.append({
                'form_field': form_field_id,
                'value': value,
                'file': file,
            })
            i += 1
        
        for response in fields_response_data:
            try:
                form_field = FormFields.objects.get(pk=response['form_field'])
            except FormFields.DoesNotExist:
                return Response({"detail": f"Form field '{response['form_field']}' not found."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                field_response = FormFieldResponse.objects.get(
                    form_submission=submission,
                    form_field=form_field
                )
                field_response.value = response.get('value', '')
                if response.get('file'):
                    field_response.file = response['file']
                field_response.updated_by = user
                field_response.save()

            except FormFieldResponse.DoesNotExist:
                FormFieldResponse.objects.create(
                    form_submission=submission,
                    form_field=form_field,
                    value=response.get('value', ''),
                    file=response.get('file', None),
                    created_by=user,
                    updated_by=user
                )

        return Response({
            "message": "Submission assigned successfully.",
            "submission_id": submission.id
        }, status=status.HTTP_201_CREATED)

    
class FormSubmissionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, submission_id):
        try:
            submission = FormSubmission.objects.get(pk=submission_id)
        except FormSubmission.DoesNotExist:
            return Response({"detail": "Submission not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FormSubmissionSerializer(submission)
        return Response(serializer.data)
    
    def patch(self, request, submission_id):
        try:
            submission = FormSubmission.objects.get(pk=submission_id)
        except FormSubmission.DoesNotExist:
            return Response({"detail": "Submission not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = FormSubmissionSerializer(submission, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSubmissionsByFormIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, form_id):
        # Retrieve all form submissions by form_id
        submissions = FormSubmission.objects.filter(project_id=project_id, form_id=form_id)

        if not submissions:
            return Response({"detail": "No submissions found for this form."}, status=status.HTTP_204_NO_CONTENT)

        # Serialize the form submissions
        serializer = FormSubmissionSerializer(submissions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProjectBySubjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        projects = Project.objects.filter(subject__id=subject_id)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class AssignmentForTeacherBySubjectView(APIView):
    serializer_class = AssignmentsForTeacher
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        submissions = FormSubmission.objects.filter(
            project__subject_id=subject_id,
            project__teacher=request.user # Filter by current logged-in teacher
        )
        serializer = AssignmentsForTeacher(submissions, many=True)
        return Response(serializer.data)
