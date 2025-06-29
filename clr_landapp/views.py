from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import login
from .models import UploadedFile, PrinterConfig
from .serializers import (LoginSerializer, UploadedFileSerializer, PrinterConfigSerializer)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Login
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "Login successful"}, status=200)
        return Response(serializer.errors, status=400)

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
        return Response(serializer.data)

    def delete(self, request):
        name = request.query_params.get('name')
        if not name:
            return Response({"error": "Name parameter is required"}, status=400)
        count, _ = UploadedFile.objects.filter(name=name).delete()
        return Response({"deleted": count}, status=200)

class DataDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, row_id):
        row = get_object_or_404(UploadedFile, id=row_id)
        serializer = UploadedFileSerializer(row)
        return Response(serializer.data)

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
