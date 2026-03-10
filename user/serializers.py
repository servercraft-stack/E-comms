from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from base.choices import UserTypeChoices, StatusChoices
from base.account_utils import complete_password_reset, email_validator, get_tokens_for_user, send_otp_email, set_user_otp, verfiy_user_otp

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "user_types", "is_active", "is_staff"]
        read_only_fields = ["id", "is_active", "is_staff"]


class UserDetialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "user_types", "is_active", "is_staff"]
        read_only_fields = ["id", "email", "is_active", "is_staff"]

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    confirm_password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "confirm_password"]

        extra_kwargs = {
            "user_type": {"default": UserTypeChoices.USER},
            "is_active": {"default": False},
        }


    def validate_email(self, value):
        if not email_validator(value):
            raise serializers.ValidationError("Invalid email format")
        return value.lower()

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        if len(data["password"]) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        validated_data["is_active"] = False
        
        user = User.objects.create_user(
            email=validated_data.pop("email"),
            password=validated_data.pop("password"),
            **validated_data
        )

        otp = set_user_otp(user)
        send_otp_email(user.id, otp, "account verification")
        return user

    