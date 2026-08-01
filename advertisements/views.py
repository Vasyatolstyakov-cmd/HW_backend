from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return []

    def update(self, request, *args, **kwargs):
        advertisement = self.get_object()
        if advertisement.creator != request.user:
            raise ValidationError('Вы не можете менять чужое объявление.')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        advertisement = self.get_object()
        if advertisement.creator != request.user:
            raise ValidationError('Вы не можете удалить чужое объявление.')
        return super().destroy(request, *args, **kwargs)
