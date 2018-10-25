from rest_framework import serializers

from ..models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="slcsd_cms:api:user-detail"
    )
    date_joined = serializers.DateTimeField(
        required=False,
        format='%b. %d, %Y, %I:%M %p'
    )
    update_date = serializers.DateTimeField(
        required=False,
        format='%b. %d, %Y, %I:%M %p'
    )

    class Meta:
        model = User
        fields = (
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
            'update_date',
        )
