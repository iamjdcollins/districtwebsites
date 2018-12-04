from rest_framework import serializers
from rest_framework.reverse import reverse

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
    canonical = serializers.SerializerMethodField()
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
    group = serializers.HyperlinkedRelatedField(
        many=False,
        view_name="slcsd_cms:api:group-detail",
        lookup_field="uuid",
        lookup_url_kwarg="uuid",
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
