from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'birth_date', 'location', 'favorite_words', 'avatar')

    gender = serializers.CharField(source='profile.gender')
    birth_date = serializers.DateField(source='profile.birth_date')
    location = serializers.CharField(source='profile.location')
    favorite_words = serializers.CharField(source='profile.favorite_words')
    avatar = serializers.CharField(source='profile.avatar')
