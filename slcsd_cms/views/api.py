from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from ..models import (
    User,
    Site,
    Domain,
)
from ..serializers import (
    UserSerializer,
    SiteSerializer,
    DomainSerializer,
)


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.get_published()
        user_type = self.request.query_params.get('type', None)
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        return queryset


class SiteViewSet(viewsets.ModelViewSet):

    queryset = Site.objects.get_published()
    serializer_class = SiteSerializer

    @action(
        methods=['get'],
        detail=True,
        url_path='domains',
        url_name="domains",
    )
    def list_domains(self, request, pk=None):
        site = self.get_object()
        queryset = Domain.objects.get_published().filter(site=site)
        serializer = DomainSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)


class DomainViewSet(viewsets.ModelViewSet):

    queryset = Domain.objects.get_published()
    serializer_class = DomainSerializer
