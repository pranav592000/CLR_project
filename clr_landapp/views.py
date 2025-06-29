from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login
from .models import UploadedFile, PrinterConfig
from .serializers import (LoginSerializer, UploadedFileSerializer, PrinterConfigSerializer)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Login
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)
            
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "message": "Login successful",
                    "token": token.key
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Upload
class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# Data Retrieve & Delete
class DataView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        name = request.query_params.get('name')
        tag = request.query_params.get('tag')
        queryset = UploadedFile.objects.all()
        if name:
            queryset = queryset.filter(name__icontains=name)
        if tag:
            queryset = queryset.filter(tag__icontains=tag)
        serializer = UploadedFileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Data view and delete
class DataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.query_params.get('name')
        tag = request.query_params.get('tag')
        queryset = UploadedFile.objects.all()
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        if tag:
            queryset = queryset.filter(tag__icontains=tag)

        serializer = UploadedFileSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({"error": "Name parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = UploadedFile.objects.filter(name=name)
        count = queryset.count()
        
        if count == 0:
            return Response({"message": "No records found with that name"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset.delete()
        return Response({"deleted": count}, status=status.HTTP_200_OK)

class DataDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, row_id):
        row = get_object_or_404(UploadedFile, id=row_id)
        serializer = UploadedFileSerializer(row)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, row_id):
        row = get_object_or_404(UploadedFile, id=row_id)
        row.delete()
        return Response({"message": f"Record with id {row_id} deleted."}, status=status.HTTP_200_OK)
# Printer config
class PrinterConfigView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = PrinterConfigSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
# Logout    
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()  # Deletes the token for the logged-in user
        except:
            return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)