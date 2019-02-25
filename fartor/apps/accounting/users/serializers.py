from rest_framework import serializers


class UserBaseSerializers(object):
    id = serializers.CharField(source='public_name', read_only=True)
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserSelfSerializers(serializers.Serializer, UserBaseSerializers):
    date_joined = serializers.DateTimeField()

    def update(self, instance, validated_data):
        raise NotImplemented

    def create(self, validated_data):
        raise NotImplemented
