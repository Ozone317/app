from rest_framework import serializers
from . import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = ["id", "email", "name", "password"]

        # We should make the password write-only; users should not be able to retrieve the password hash
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {
                    "input-type": "password"
                }
            }
        }

        # If we simply let this serializer call its create method, the password won't be stored as a hash.
        # We should override the create function so that the password gets created as a hash
        # instead of being stored as text, when a user is created.
        # To override the create function, we should call our create_user function defined in the
        # UserProfileManager class, which we have already linked to our UserProfile class using the following property:
        # objects = UserProfileManager()

        def create(self, validated_data):
            """Create and return a new user, with the password being saved as a hash"""
            user = models.UserProfile.objects.create_user(
                email=validated_data["email"],
                name=validated_data["name"],
                password=validated_data["password"]
            )

            return user


class ProfileFeedItemSerializers(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ["id", "user", "status_text", "created_on"]
        
        extra_kwargs = {
            "user": {
                "read_only": True
            }
        }