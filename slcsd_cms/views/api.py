from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.db.models import Prefetch

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import APIRootView as APIRootViewBase

from django.shortcuts import get_object_or_404

from ..models import (
    User,
    Site,
    Domain,
    Group,
)
from ..serializers import (
    UserSerializer,
    SiteSerializer,
    DomainSerializer,
    GroupSerializer,
)


class APIRootView(LoginRequiredMixin, APIRootViewBase):
    pass


class UserViewSet(LoginRequiredMixin, viewsets.ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.get_published()
        user_type = self.request.query_params.get('type', None)
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        return queryset


class SiteViewSet(LoginRequiredMixin, viewsets.ModelViewSet):

    queryset = Site.objects.get_published().prefetch_related('domains').order_by('-management', 'title')
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


class DomainViewSet(LoginRequiredMixin, viewsets.ModelViewSet):

    queryset = Domain.objects.get_published()
    serializer_class = DomainSerializer

class GroupViewSet(LoginRequiredMixin, viewsets.ModelViewSet):

    lookup_field = 'uuid'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer