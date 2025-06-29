from rest_framework import serializers
from .models import UploadedFile, PrinterConfig
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    # def validate(self, data):
    #     user = authenticate(**data)
    #     if user and user.is_staff:
    #         return user
    #     raise serializers.ValidationError("Invalid credentials or not staff")

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'

class PrinterConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrinterConfig
        fields = '__all__'
