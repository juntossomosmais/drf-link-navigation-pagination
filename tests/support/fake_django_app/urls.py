from django.urls import include
from django.urls import path
from rest_framework import routers
from tests.support.fake_django_app.views import TestViewSet

router = routers.DefaultRouter()
router.register(r"data", TestViewSet)

urlpatterns = [path(r"", include(router.urls))]
