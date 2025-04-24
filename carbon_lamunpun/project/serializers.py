from rest_framework import serializers
from .models import Project, FormSubmission, FormFieldResponse
from forms.serializers import FormsSerializer, SubjectSerializer, FormsFieldsSerializer
from shared.serializers import FormSubmissionSerializer, FormFieldResponseSerializer
from forms.models import FormFields, Subject
from auth.serializers import UserSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):

    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    updated_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    # Use nested serializers for GET (list/detail)
    subject_detail = SubjectSerializer(source='subject', read_only=True)
    student_detail = UserSerializer(source='student', read_only=True)
    # teacher_detail = UserSerializer(source='teacher', read_only=True)
    # created_by_detail = UserSerializer(source='created_by', read_only=True)
    # updated_by_detail = UserSerializer(source='updated_by', read_only=True)
    class Meta:
        model = Project
        fields = '__all__'
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if self.context.get('request') and self.context['request'].method == 'GET':
            representation.pop('subject')
            representation.pop('student')
            representation.pop('teacher')
            representation.pop('created_by')
            representation.pop('updated_by')
            
        return representation

class FormFieldResponseSerializer(serializers.ModelSerializer):
    form_field = FormsFieldsSerializer(read_only=True)  

    class Meta:
        model = FormFieldResponse
        fields = '__all__'

class FormSubmissionSerializer(serializers.ModelSerializer):
    form = FormsSerializer(read_only=True)
    # fix relation
    fieldsResponse = FormFieldResponseSerializer(many=True, source='formfieldresponse_set')
    class Meta:
        model = FormSubmission
        fields = '__all__'
    
    def update(self, instance, validated_data):
        request_user = self.context['request'].user
        fields_data = validated_data.pop('fieldsResponse', [])

        # Update main FormSubmission fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_by = request_user
        instance.save()

        for field_data in fields_data:
            response_obj = field_data.pop('form_field_res', None)
            response_id = response_obj.id if isinstance(response_obj, FormFieldResponse) else response_obj

            if response_id:
                # Update existing FormFieldResponse
                try:
                    response = FormFieldResponse.objects.get(id=response_id, form_submission=instance)
                    for key, value in field_data.items():
                        setattr(response, key, value)
                    response.updated_by = request_user
                    response.save()
                except FormFieldResponse.DoesNotExist:
                    continue

        return instance


