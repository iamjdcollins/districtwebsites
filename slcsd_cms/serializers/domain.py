from rest_framework import serializers

from ..models import (
    Domain,
    User,
    Site,
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


class ListDomainSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:domain-detail"
    )

    class Meta:
        model = Domain
        fields = [
            'url',
            'pk',
            'domain',
            'environment',
            'canonical',
            'published',
        ]


class DomainSerializer(ListDomainSerializer):

    site = NestedSiteSerializer(
        many=False,
        read_only=True,
    )
    create_user = NestedUserSerializer(
        many=False,
        read_only=True,
    )
    update_user = NestedUserSerializer(
        many=False,
        read_only=True,
    )
    delete_user = NestedUserSerializer(
        many=False,
        read_only=True,
    )

    class Meta:
        model = Domain
        fields = [
            'url',
            'pk',
            'domain',
            'environment',
            'site',
            'canonical',
            'published',
            'create_date',
            'create_user',
            'update_date',
            'update_user',
            'delete_date',
            'delete_user',
        ]
