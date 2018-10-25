from rest_framework import serializers

from ..models import Domain, Site


class DomainSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:domain-detail"
    )
    site = serializers.HyperlinkedRelatedField(
        view_name="slcsd_cms:api:site-detail",
        queryset=Site.objects.all(),
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
