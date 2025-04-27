from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from forms.models import Subject
from project.models import Project
from .serializers import RegisterSerializer, LoginSerializer, TestSerializer, UserSerializer, RoleListSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView, ListAPIView

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            subject = Project.objects.filter(created_by=user).first()
            project = Project.objects.filter(created_by=user).first()

            role = None
            if user.groups.filter(name="Teacher").exists():
                role = "Teacher"
            elif user.groups.filter(name="Student").exists():
                role = "Student"
            else:
                role = "Admin" 
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': role,
                },
                'own_subject': subject.id if subject else None,
                'own_project': project.id if project else None
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)
        

class TeacherView(ListCreateAPIView):
    queryset = User.objects.filter(groups__name='Teacher') # fillter group user is teacher
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
class RoleListView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = RoleListSerializer
    # permission_classes = [IsAuthenticated]




# TestSerializer
class TestView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = TestSerializer
    # permission_classes = [IsAuthenticated]
    