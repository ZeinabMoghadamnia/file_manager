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
