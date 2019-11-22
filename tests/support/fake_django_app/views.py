from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from tests.support.fake_django_app.models import TestModel


class TestSerializer(ModelSerializer):
    class Meta:
        model = TestModel
        fields = "__all__"


class TestViewSet(ReadOnlyModelViewSet):
    queryset = TestModel.objects.all()
    serializer_class = TestSerializer
    ordering = "created_at"
