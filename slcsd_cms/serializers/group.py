from rest_framework import serializers

from ..models import Group


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:group-detail",
        lookup_field='uuid',
        lookup_url_kwarg='uuid',
    )

    class Meta:
        model = Group
        fields = [
            'url',
            'uuid',
            'title',
            'description',
        ]
