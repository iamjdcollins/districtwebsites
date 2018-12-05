from rest_framework import serializers
from rest_framework.reverse import reverse

from ..models import (
    Site,
    Domain,
    Group
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
            'pk',
        )


class SiteSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:site-detail"
    )
    domains = NestedDomainSerializer(
        many=True,
        read_only=True
    )
    canonical = serializers.SerializerMethodField()
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
            'update_date',
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
