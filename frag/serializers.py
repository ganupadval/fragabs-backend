from rest_framework import serializers
from .models import Frags


class FragSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frags
        fields = '__all__'

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frags
        fields = ('title',)