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
            'domains',
            'update_date',
        )
