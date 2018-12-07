from rest_framework import serializers

from ..models import User


class NestedUserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:user-detail"
    )

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
        )


class ListUserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:user-detail"
    )
    date_joined = serializers.DateTimeField(
        required=False,
        format='%b. %d, %Y, %I:%M %p'
    )

    class Meta:
        model = User
        fields = [
            'url',
            'pk',
            'username',
            'first_name',
            'last_name',
            'date_joined',
        ]


class UserSerializer(ListUserSerializer):

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
    update_date = serializers.DateTimeField(
        required=False,
        format='%b. %d, %Y, %I:%M %p'
    )

    class Meta:
        model = User
        fields = [
            'url',
            'pk',
            'sync_uuid',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'user_type',
            'date_joined',
            'published',
            'create_date',
            'create_user',
            'update_date',
            'update_user',
            'delete_date',
            'delete_user',
        ]
