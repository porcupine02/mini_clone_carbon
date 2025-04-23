
from rest_framework import serializers
from project.models import FormSubmission, FormFieldResponse

class FormSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSubmission
        fields = '__all__'

class FormFieldResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormFieldResponse
        fields = '__all__'