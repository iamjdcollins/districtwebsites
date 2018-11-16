from rest_framework import serializers

from ..models import Site, Domain


class SiteSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:site-detail"
    )
    canonical = serializers.HyperlinkedRelatedField(
        view_name="slcsd_cms:api:domain-detail",
        read_only=True,
        lookup_field="uuid",
        lookup_url_kwarg="pk",
    )
    development_canonical = serializers.HyperlinkedRelatedField(
        view_name="slcsd_cms:api:domain-detail",
        read_only=True,
        lookup_field="uuid",
        lookup_url_kwarg="pk",
    )
    testing_canonical = serializers.HyperlinkedRelatedField(
        view_name="slcsd_cms:api:domain-detail",
        read_only=True,
        lookup_field="uuid",
        lookup_url_kwarg="pk",
    )
    production_canonical = serializers.HyperlinkedRelatedField(
        view_name="slcsd_cms:api:domain-detail",
        read_only=True,
        lookup_field="uuid",
        lookup_url_kwarg="pk",
    )
    domains = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="slcsd_cms:api:domain-detail",
        lookup_field="uuid",
        lookup_url_kwarg="pk",
        read_only=True,
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
            'canonical',
            'development_canonical',
            'testing_canonical',
            'production_canonical',
            'domains',
            'update_date',
        )
