from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True} # Tell DRF to not include password in returned serialized output. Noone can see it.
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data) # create_user already handles password hashing
        return user