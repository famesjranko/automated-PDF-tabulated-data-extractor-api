"""
urls.py
    Written by: Andrew McDonald
    Initial: 03.08.21
    Updated: 02.09.21
    version: 1.3

Logic:
    Handles http request addressing
"""

from django.urls import include, path
from rest_framework import routers
from . import views
from .views import *
from .views import UploadView

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


# setup api router and register models, has automatic URL routing.
router = routers.DefaultRouter()
router.register(r"reports", views.ReportViewSet)
router.register(r"extracted", views.ExtractedViewSet)

# setup url paths for user defines routes
urlpatterns = [
    path("", include(router.urls)),
    url(r"^upload/$", UploadView.as_view(), name="upload"),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # attach media storage for file access
