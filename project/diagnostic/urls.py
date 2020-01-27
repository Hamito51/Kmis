from django.urls import path

from .views import DiagnosticView


app_name = "diagnostics"

urlpatterns = [
		path('diagnostics/', DiagnosticView.as_view()),
]