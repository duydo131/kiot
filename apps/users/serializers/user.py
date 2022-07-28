from rest_framework import serializers

from apps.users.models.user import User
from config.settings.dev import DAYTIME_FORMAT
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
    username = serializers.CharField(read_only=True)
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
    total_order = serializers.IntegerField(read_only=True)
    total_money = serializers.IntegerField(read_only=True)
    total_revenue = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        user_id_to_total_product = self.context.get('user_id_to_total_product')
        user_id_to_total_money = self.context.get('user_id_to_total_money')
        user_id_to_total_order = self.context.get('user_id_to_total_order')
        user_id_to_total_revenue = self.context.get('user_id_to_total_revenue')

        if isinstance(user_id_to_total_product, dict):
            instance.total_product = user_id_to_total_product.get(instance.id, 0)

        if isinstance(user_id_to_total_money, dict):
            instance.total_money = user_id_to_total_money.get(instance.id, 0)

        if isinstance(user_id_to_total_order, dict):
            instance.total_order = user_id_to_total_order.get(instance.id, 0)

        if isinstance(user_id_to_total_revenue, dict):
            instance.total_revenue = user_id_to_total_revenue.get(instance.id, 0)

        return super(UserReadOnlySerializer, self).to_representation(instance)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        password = data.get('password')
        new_password = data.get('new_password')
        if password == new_password:
            raise serializers.ValidationError("Mật khẩu mới trùng với mật khẩu cũ")

        return data


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
    type = serializers.CharField(required=False)
    value = serializers.IntegerField(required=False)
    started_at_from = serializers.DateTimeField(required=False, input_formats=[DAYTIME_FORMAT])
    ended_at_to = serializers.DateTimeField(required=False, input_formats=[DAYTIME_FORMAT])

    def validate(self, data):
        type_filter = data.get('type')
        value = data.get('value', 0)
        if type_filter is None and value == 0:
            return data
        if type_filter != 'all' and value < 0:
            raise serializers.ValidationError("Lỗi hệ thống!")

        return data
