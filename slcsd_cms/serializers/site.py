from rest_framework import serializers

from ..models import Site


class SiteSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:site-detail"
    )
    domains = serializers.HyperlinkedIdentityField(
        many=True,
        view_name="slcsd_cms:api:domain-detail",
        # queryset=Domain.objects.all(),
    )

    class Meta:
        model = Site
        fields = (
            'url',
            'pk',
            'title',
            'description',
            'management',
            'domains',
        )
