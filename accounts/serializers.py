from rest_framework import serializers
from .models import User, UserProfile, CompanyProfile
from .tasks import send_activation_code_celery


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']


class UserSignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=5, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'phone_number']

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
        )
        user.set_password(self.validated_data['password'])
        user.is_user = True
        user.save()
        UserProfile.objects.create(user=user)
        return user

    def create(self, validated_data):
        user = UserProfile.objects.create(**validated_data)
        send_activation_code_celery.delay(user.email, user.user.activation_code)
        return user


class CompanySignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=5, required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm'
        ]

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            phone_number=self.validated_data['phone_number'],
        )
        user.set_password(self.validated_data['password'])
        user.is_driver = True
        user.save()
        CompanyProfile.objects.create(user=user)
        return user

    def create(self, validated_data):
        user = CompanyProfile.objects.create(**validated_data)
        user.create_activation_code()
        send_activation_code_celery(user.email, user.user.activation_code)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=5, write_only=True)
    new_password = serializers.CharField(required=True, min_length=5, write_only=True)
    new_password_confirm = serializers.CharField(required=True, min_length=5, write_only=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Старый пароль введен неверно')
        return old_password

    def validate(self, attrs):
        p1 = attrs['new_password']
        p2 = attrs['new_password_confirm']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data['new_password'])
        user.save(update_fields=['password'])
        return user
