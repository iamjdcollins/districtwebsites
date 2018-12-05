from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import (
    Site,
    User,
    Domain,
    Group
)


class NestedUserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:user-detail'"
    )

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
        )


class NestedDomainSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:domain-detail",
    )

    class Meta:
        model = Domain
        fields = (
            'url',
            'pk',
            'domain',
            'environment',
            'canonical',
        )


class NestedGroupSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:group-detail",
        lookup_field='uuid',
        lookup_url_kwarg='uuid',
    )

    class Meta:
        model = Group
        fields = (
            'url',
            'uuid',
            'title',
            'description',
        )


class SiteSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:site-detail"
    )
    domains = NestedDomainSerializer(
        many=True,
        read_only=True
    )
    canonical = NestedDomainSerializer(
        many=False,
        read_only=True
    )
    development_canonical = NestedDomainSerializer(
        many=False,
        read_only=True,
    )
    testing_canonical = NestedDomainSerializer(
        many=False,
        read_only=True,
    )
    production_canonical = NestedDomainSerializer(
        many=False,
        read_only=True,
    )
    group = NestedGroupSerializer(
        many=False,
        read_only=True,
    )
    create_user = NestedUserSerializer(
        many=False,
        read_only=True,
    )
    update_user = NestedUserSerializer(
        many=False,
        read_only=True,
    )
    delete_user = NestedUserSerializer(
        many=False,
        read_only=True,
    )
    update_date = serializers.DateTimeField(
        required=False,
        format='%b. %d, %Y, %I:%M %p'
    )

    class Meta:
        model = Site
        fields = (
            'url',
            'pk',
            'title',
            'description',
            'management',
            'canonical',
            'development_canonical',
            'testing_canonical',
            'production_canonical',
            'domains',
            'group',
            'published',
            'create_date',
            'create_user',
            'update_date',
            'update_user',
            'delete_date',
            'delete_user',
        )

    def get_canonical(self, obj):
        request = self.context['request'] if 'request' in self.context else \
            None
        url = reverse(
            'slcsd_cms:api:domain-detail',
            args=[obj.canonical_id],
            request=request
        )
        return url if obj.canonical_id else None
