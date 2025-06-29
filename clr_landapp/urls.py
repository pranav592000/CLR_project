from django.urls import path
from .views import (
    LoginAPIView, FileUploadView, DataView,
    DataDetailView, PrinterConfigView
)

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view()),
    path('upload/', FileUploadView.as_view()),
    path('data/', DataView.as_view()),
    path('data/<int:row_id>/', DataDetailView.as_view()),
    path('printer-config/', PrinterConfigView.as_view()),
]
