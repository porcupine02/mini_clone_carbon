from rest_framework import status
from .models import Forms, FormFields, Subject, FormSubject
from .serializers import FormsSerializer, FormsFieldsSerializer, FormsSubjectLinkSerializer, SubjectSerializer, FormDetailSerializer, FormsSubjectSerializer, FormsSubjectDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

class CreateFormAndFormFields(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        form_data = request.data.get('form')
        fields_data = request.data.get('fields', [])

        # Step 1: Create Form
        form_serializer = FormsSerializer(data=form_data)
        if form_serializer.is_valid():
            form = form_serializer.save()

            # Step 2: Create Form Fields
            created_fields = []
            for field in fields_data:
                print('field', field)
                field['form'] = form.id  # link to the created form
                field['created_by'] = request.data.get('created_by')
                field['updated_by'] = request.data.get('updated_by')
                field_serializer = FormsFieldsSerializer(data=field)
                if field_serializer.is_valid():
                    field_serializer.save()
                    created_fields.append(field_serializer.data)
                else:
                    return Response({
                        "error": "Invalid field data",
                        "details": field_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)

            # Step 3: Return
            return Response({
                "form": form_serializer.data,
                "fields": created_fields
            }, status=status.HTTP_201_CREATED)

        return Response({
            "error": "Invalid form data",
            "details": form_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class FormsView(ListCreateAPIView):
    queryset = Forms.objects.all()
    serializer_class = FormsSerializer
    permission_classes = [IsAuthenticated]
    

# Use by id
class FormsByIdView(RetrieveUpdateDestroyAPIView):
    queryset = Forms.objects.all()
    serializer_class = FormDetailSerializer
    permission_classes = [IsAuthenticated]
    

# ----------------------------------------------------- #
class FormFieldsView(ListCreateAPIView):
    queryset = FormFields.objects.all()
    serializer_class = FormsFieldsSerializer
    permission_classes = [IsAuthenticated]


class FormFieldsByIdView(RetrieveUpdateDestroyAPIView):
    queryset = FormFields.objects.all()
    serializer_class = FormsFieldsSerializer
    permission_classes = [IsAuthenticated]


# ----------------------------------------------------- #
class SubjectView(ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]


class SubjectByIdView(RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LinkFormToSubjectView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, subject_id):
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)

        form_ids = request.data.get("form_ids", [])

        if not isinstance(form_ids, list):

            return Response({"error": "form_ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        forms = Forms.objects.filter(id__in=form_ids)
        subject.forms.add(*forms)
        
        # result = SubjectSerializer(subject).data
        return Response({
            "message": f"{len(forms)} form(s) added to subject {subject_id}",
            # "result": result
        }, status=status.HTTP_200_OK)
    


    def delete(self, request, subject_id):
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({"error": "Subject not found"}, status=status.HTTP_404_NOT_FOUND)

        form_ids = request.data.get("form_ids", [])

        if not isinstance(form_ids, list):
            return Response({"error": "form_ids must be a list"}, status=status.HTTP_400_BAD_REQUEST)

        forms = Forms.objects.filter(id__in=form_ids)
        subject.forms.remove(*forms)
        subject.save()
        # result = SubjectSerializer(subject).data  
        return Response({
            "message": f"{len(forms)} form(s) removed from subject {subject_id}",
            # "subject": result
        }, status=status.HTTP_200_OK)


class AddMainFormByIdView(RetrieveUpdateDestroyAPIView):
    queryset = FormSubject.objects.all()
    serializer_class = FormsSubjectSerializer
    permission_classes = [IsAuthenticated]
    

class FormsSubjectView(ListCreateAPIView):
    queryset = FormSubject.objects.all()
    serializer_class = FormsSubjectLinkSerializer
    permission_classes = [IsAuthenticated]


    
# class FormsSubjectBySubjIdView(ListCreateAPIView):
#     # Get Form for display main : field response
#     queryset = FormSubject.objects.all()
#     serializer_class = FormsSubjectDetailSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         subject_id = self.kwargs['pk']
#         return FormSubject.objects.filter(subject_id=subject_id)
    
    
class MainFormBySubjectView(ListAPIView):
    serializer_class = FormsSubjectDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        return FormSubject.objects.filter(subject_id=subject_id, main=True)

class FormsBySubjectView(ListAPIView):
    serializer_class = FormsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        return Forms.objects.filter(subjects__id=subject_id).annotate(
            submissions_count=Count('formsubmissions')
        ).order_by('-created_at')
    
    
