from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from forms.models import Forms
from project.models import FormSubmission

def health_check(request):
    return JsonResponse({"status": "ok"})


class FormsWithSubmissionsBySubjectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, subject_id):
        forms = Forms.objects.filter(subjects__id=subject_id)

        data = []
        for form in forms:
            submission_count = FormSubmission.objects.filter(form=form).count()
            data.append({
                "form_id": form.id,
                "title": form.title,
                "description": form.description,
                "countSubmissions": submission_count
            })

        return Response(data)