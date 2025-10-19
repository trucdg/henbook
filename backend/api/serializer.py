from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True} # Tell DRF to not include password in returned serialized output. Noone can see it.
        }

    def create(self, validated_data):
        ## We override the create method to hash the password properly
        user = User.objects.create_user(**validated_data) # create_user already handles password hashing
        return user

class NoteSerializer(serializers.ModelSerializer):
    ## Django ModelSerializer automatically creates objects for you
    class Meta:
        model = Note
        fields = ['id','author', 'content', 'created_at']
        read_only_fields = ['author']
