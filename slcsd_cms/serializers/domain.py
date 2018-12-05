from rest_framework import serializers

from ..models import Domain, Site


class NestedSiteSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:domain-detail"
    )

    class Meta:
        model = Site
        fields = (
            'url',
            'pk',
        )



class DomainSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:domain-detail"
    )
    site = NestedSiteSerializer(
        many=False,
        read_only=True,
    )

    class Meta:
        model = Domain
        fields = (
            'url',
            'pk',
            'domain',
            'environment',
            'site',
            'canonical',
        )
