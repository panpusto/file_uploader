from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterAccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=get_user_model().objects.all(),
            message='Account with this email address already exists.')]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password])
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password',
            'password2'
        )
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."}
            )
        return attrs
     
    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user