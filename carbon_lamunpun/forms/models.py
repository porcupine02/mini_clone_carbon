from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# from django.conf import settings
# User = settings.AUTH_USER_MODEL

class Forms(models.Model):
    # id = models.IntegerField(max_length=5)
    # name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    main = models.IntegerField(blank=True, null=True)
    # subjects = models.ManyToManyField('Subject', related_name='forms', blank=True)
    subjects = models.ManyToManyField('Subject', through='FormSubject', related_name='forms', blank=True)
    created_by = models.ForeignKey(User, related_name='form_created', on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='form_updated', on_delete=models.CASCADE, null=True)

class FormFields(models.Model):
    TEXT = 'text'
    SELECT = 'select'
    FILE = 'file'
    FIELD_TYPES = [
        (TEXT, 'Text'),
        (SELECT, 'Select'),
        (FILE, 'File'),
    ]
    # form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    form = models.ForeignKey(Forms, on_delete=models.CASCADE, related_name='formfields')  
    label = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=FIELD_TYPES)
    optionRaw = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='formfield_created', on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='formfield_updated', on_delete=models.CASCADE, null=True)

class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, null=True)
    # forms = models.ManyToManyField('Forms', related_name='subjects')
    created_by = models.ForeignKey(User, related_name='subject_created', on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    updated_by = models.ForeignKey(User, related_name='subject_updated', on_delete=models.CASCADE, null=True)

class FormSubject(models.Model):
    form = models.ForeignKey('Forms', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    main = models.BooleanField(default=False)

    class Meta:
        unique_together = ('form', 'subject')
