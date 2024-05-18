from rest_framework import serializers

# from .models import File
from applications.storage.models import File, Folder


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


class EditFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = [
            "name",
        ]

class EditFolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = [
            "name",
        ]


class UploadFileSerializer(serializers.Serializer):
    name = serializers.CharField()
    content = serializers.FileField()
    folder = serializers.PrimaryKeyRelatedField(
        queryset=Folder.objects.all(), required=False
    )

    def create(self, validated_data):
        return File.objects.create(**validated_data)


class FolderSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()

    def get_create_time(self, obj):
        return obj.create_time.strftime("%H:%M")

    class Meta:
        model = Folder
        fields = [
            "id",
            "name",
            "create_date",
            "create_time",
            "user",
            "size",
        ]


class CreateFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ["id", "name", "parent"]
