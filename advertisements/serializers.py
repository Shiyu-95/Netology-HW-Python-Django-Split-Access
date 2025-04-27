from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user
        open_advertisements_count = Advertisement.objects.filter(creator=user, status='OPEN').count()
        if open_advertisements_count >= 10 and data.get('status') == 'OPEN':
            raise serializers.ValidationError("У вас не может быть больше 10 открытых объявлений.")
        return data
