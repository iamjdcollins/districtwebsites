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
        queryset = queryset.select_related(
            'create_user',
            'update_user',
            'delete_user',
        )
        user_type = self.request.query_params.get('type', None)
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        return queryset


class SiteViewSet(LoginRequiredMixin, viewsets.ModelViewSet):

    serializer_class = SiteSerializer

    def get_queryset(self):
        queryset = Site.objects.get_published()
        queryset = queryset.select_related(
            'group',
            'development_canonical',
            'testing_canonical',
            'production_canonical',
            'create_user',
            'update_user',
            'delete_user',
        )
        queryset = queryset.prefetch_related('domains')
        queryset = queryset.order_by('-management', 'title')
        return queryset

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

    serializer_class = DomainSerializer

    def get_queryset(self):
        queryset = Domain.objects.get_published()
        queryset = queryset.select_related(
            'site'
            'create_user',
            'update_user',
            'delete_user',
        )
        return queryset


class GroupViewSet(LoginRequiredMixin, viewsets.ModelViewSet):

    lookup_field = 'uuid'
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = Group.objects.all()
        queryset = queryset.select_related(
            'site',
        )
        queryset = queryset.order_by('-site__management', 'title')
        return queryset
