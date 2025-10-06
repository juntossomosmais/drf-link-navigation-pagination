from django.urls import include
from django.urls import path
from rest_framework import routers
from tests.support.fake_django_app.views import TestListViewSet, TestViewSet

router = routers.DefaultRouter()
router.register(r"data", TestViewSet)

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"data-no-slash", TestListViewSet.as_view(), name='data-no-slash'),
    path(r"data-with-slash/", TestListViewSet.as_view(), name='data-with-slash'),
]
