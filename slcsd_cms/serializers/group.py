from rest_framework import serializers

from ..models import (
    Group,
    Site,
    User,
)


class NestedUserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:user-detail'"
    )

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
        )


class NestedSiteSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:domain-detail"
    )

    class Meta:
        model = Site
        fields = (
            'url',
            'pk',
            'title',
            'description',
            'management',
        )


class ListGroupSerializer(serializers.HyperlinkedModelSerializer):

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


class GroupSerializer(ListGroupSerializer):

    site = NestedSiteSerializer(
        many=False,
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
