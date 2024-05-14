from rest_framework import serializers
# from .models import File
from applications.storage.models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class DeleteSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
