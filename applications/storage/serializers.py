from rest_framework import serializers

# from .models import File
from applications.storage.models import File


class FileSerializer(serializers.ModelSerializer):
    upload_time = serializers.SerializerMethodField()

    def get_upload_time(self, obj):
        return obj.upload_time.strftime("%H:%M")

    class Meta:
        model = File
        fields = [
            "id",
            "name",
            "content",
            "upload_date",
            "upload_time",
            "size",
            "type",
            "thumbnail",
            "user",
            "folder",
        ]


class DeleteSerializer(serializers.Serializer):
    file_id = serializers.IntegerField()
    
class UploadFile(serializers.Serializer):
    name = serializers.CharField()
    content = serializers.FileField()
    
    def create(self, validated_data):
        """
        Create and return a new `UploadFile` instance, given the validated data.
        """
        return File.objects.create(**validated_data)
