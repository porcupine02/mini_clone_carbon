from rest_framework import serializers
from project.models import FormFieldResponse, FormSubmission
from shared.serializers import FormSubmissionSerializer, FormFieldResponseSerializer
from .models import Forms, FormFields, Subject, FormSubject

class FormsFieldsSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(
        queryset=Forms.objects.all(),
        many=False,
        required=False
    )

    class Meta:
        model = FormFields
        fields = '__all__'
        # exclude = ['form']  #field exten from form


class FormsSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        many=True,
        required=False
    )
    submissions_count = serializers.IntegerField(read_only=True)
    # fields = FormsFieldsSerializer(many=True, write_only=True)
    

    class Meta:
        model = Forms
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    forms = FormsSerializer(many=True, read_only=True)  # Shows forms related to the subject

    class Meta:
        model = Subject
        fields = '__all__'
    def validate(self, attrs):
        if self.instance is None:
            missing_fields = {}
            required_on_create = ['created_by', 'updated_by']

            for field in required_on_create:
                if not attrs.get(field):
                    missing_fields[field] = 'This field is required.'

            if missing_fields:
                raise serializers.ValidationError(missing_fields)
        return attrs

class FormDetailSerializer(serializers.ModelSerializer):
    # Reverse relation is accessed by 'formfields' from Forms model
    fields = FormsFieldsSerializer(many=True, read_only=True, source='formfields')

    class Meta:
        model = Forms
        fields = [
            'id', 'title', 'description', 'main', 'created_at', 'updated_at', 
            'created_by', 'updated_by', 'fields'
        ]
    def update(self, instance, validated_data):

        formfields_data = validated_data.pop('formfields', [])

        # Update form instance
        instance = super().update(instance, validated_data)

        for field_data in formfields_data:
            FormFields.objects.create(form=instance, **field_data)
        
        return instance

class FormsSubjectSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(
        queryset=Forms.objects.all(),
        many=False,
        required=False
    )

    class Meta:
        model = FormSubject
        fields = '__all__'


class FormsSubjectLinkSerializer(serializers.ModelSerializer):
    form = serializers.PrimaryKeyRelatedField(
        queryset=Forms.objects.all()
    )
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all()
    )
    class Meta:
        model = FormSubject
        fields = '__all__'

class FormsSubjectDetailSerializer(serializers.ModelSerializer):
    form = FormsSerializer(read_only=True)
    fieldsResponse = FormsFieldsSerializer(many=True, read_only=True, source='form.formfields')

    submission = serializers.SerializerMethodField()
    field_responses = serializers.SerializerMethodField()

    class Meta:
        model = FormSubject
        fields = ['id', 'form', 'main', 'subject', 'fieldsResponse', 'submission', 'field_responses']

    def get_submission(self, obj):
        # submissions = FormSubmission.objects.filter(form=obj.form, subject=obj.subject)
        submissions = FormSubmission.objects.filter(form=obj.form, project__subject=obj.subject)
        return FormSubmissionSerializer(submissions, many=True).data

    def get_field_responses(self, obj):
        # FormFieldResponse -> form_submission -> form
        fieldresponses = FormFieldResponse.objects.filter(form_submission__form=obj.form)
        return FormFieldResponseSerializer(fieldresponses, many=True).data
