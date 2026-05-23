
from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):

    confirm_pass = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_pass"]

        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_pass")

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")

        # check username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")

        if not password:
            raise serializers.ValidationError("Password is required")

        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_pass")

        user = User(
            username=validated_data["username"],  # ✅ correct
            email=validated_data["email"]
        )

        user.set_password(validated_data["password"])
        user.save()

        return user




class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "email",
            "is_staff"
        ]

