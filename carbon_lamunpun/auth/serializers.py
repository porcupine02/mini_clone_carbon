from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[('Student', 'Student'), ('Teacher', 'Teacher'), ('Admin', 'Admin')], write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Passwords must match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  
        role = validated_data.pop('role')
        user = User.objects.create_user(**validated_data)

        # Ensure the group exists and create it if necessary
        group, created = Group.objects.get_or_create(name=role.capitalize())  # Creates the group if not exists

        # Add the user to the group (role assignment)
        user.groups.add(group)
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")

        token, created = Token.objects.get_or_create(user=user)
        attrs['token'] = token.key  # Store the token to be returned
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
 
class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

