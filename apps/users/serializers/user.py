from rest_framework import serializers

from apps.users.models.user import User
from core.serializer import BaseSerializer, UUIDArrayField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["deleted", "password"]
        read_only_fields = ["created_at", "updated_at"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["deleted", "password"]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        if attrs.get('username') is not None and attrs.get('name') is None:
            attrs['name'] = attrs.get('username')
        return attrs


class UserReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    fid = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    address = serializers.CharField(read_only=True)
    avatar_url = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    total_terminal = serializers.IntegerField(read_only=True)
    total_product = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        user_id_to_total_product = self.context.get('user_id_to_total_product')
        if isinstance(user_id_to_total_product, dict):
            instance.total_product = user_id_to_total_product.get(instance.id, 0)
        return super(UserReadOnlySerializer, self).to_representation(instance)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class RegisterSerializer(serializers.Serializer):
    role = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        role = data.get('role')
        if not self.instance and User.objects.filter(email=email, role=role):
            raise serializers.ValidationError("Email Already")

        return data


class UserListInputSerializer(BaseSerializer):
    ids = UUIDArrayField(required=False)
    role = serializers.CharField(required=False)

