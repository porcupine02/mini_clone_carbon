# # Project

# class FormFieldResponseSerializer(serializers.ModelSerializer):
#     form_field = FormsFieldsSerializer(read_only=True)  

#     class Meta:
#         model = FormFieldResponse
#         fields = '__all__'


# class FormSubmissionSerializer(serializers.ModelSerializer):
#     form = FormsSerializer(read_only=True)
#     # fix relation
#     fieldsResponse = FormFieldResponseSerializer(many=True, source='formfieldresponse_set')
#     class Meta:
#         model = FormSubmission
#         fields = '__all__'
    
#     def update(self, instance, validated_data):
#         request_user = self.context['request'].user
#         fields_data = validated_data.pop('fieldsResponse', [])

#         # Update main FormSubmission fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.updated_by = request_user
#         instance.save()

#         for field_data in fields_data:
#             response_obj = field_data.pop('form_field_res', None)
#             response_id = response_obj.id if isinstance(response_obj, FormFieldResponse) else response_obj

#             if response_id:
#                 # Update existing FormFieldResponse
#                 try:
#                     response = FormFieldResponse.objects.get(id=response_id, form_submission=instance)
#                     for key, value in field_data.items():
#                         setattr(response, key, value)
#                     response.updated_by = request_user
#                     response.save()
#                 except FormFieldResponse.DoesNotExist:
#                     continue

#         return instance

