from rest_framework import serializers

from ..models import Site, Domain


class SiteSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:site-detail"
    )
    domains = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="slcsd_cms:api:domain-detail",
        lookup_field="uuid",
        lookup_url_kwarg="pk",
        read_only=True,
        # queryset=Domain.objects.all(),
    )
    development_canonical = serializers.HyperlinkedRelatedField(
        many=False,
        view_name="slcsd_cms:api:domain-detail",
        lookup_field="pk",
        lookup_url_kwarg="pk",
        read_only=True,
    )
    testing_canonical = serializers.HyperlinkedRelatedField(
        many=False,
        view_name="slcsd_cms:api:domain-detail",
        lookup_field="pk",
        lookup_url_kwarg="pk",
        read_only=True,
    )
    production_canonical = serializers.HyperlinkedRelatedField(
        many=False,
        view_name="slcsd_cms:api:domain-detail",
        lookup_field="pk",
        lookup_url_kwarg="pk",
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
            'development_canonical',
            'testing_canonical',
            'production_canonical',
            'domains',
            'update_date',
        )
