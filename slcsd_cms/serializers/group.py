from rest_framework import serializers

from ..models import Group


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:group-detail",
        lookup_field='uuid',
        lookup_url_kwarg='uuid',
    )
    site = serializers.HyperlinkedRelatedField(
        many=False,
        view_name="slcsd_cms:api:site-detail",
        lookup_field="pk",
        lookup_url_kwarg="pk",
        read_only=True,
    )

    class Meta:
        model = Group
        fields = [
            'url',
            'uuid',
            'title',
            'description',
            'site',
        ]
