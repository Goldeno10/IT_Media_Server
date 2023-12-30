from rest_framework import serializers
from .models import Media

class MediaSerializer(serializers.ModelSerializer):
    """Serializer for media files"""
    file_type = serializers.CharField(max_length=50, read_only=True)
    title = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = Media
        fields = ['id', 'title', 'description', 'file', 'uploaded_at', 'file_type']
        read_only_fields = ['id', 'uploaded_at', 'file_type', 'thumbnail', 'owner', 'file_size']


class RetrieveMediaSerializer(serializers.ModelSerializer):
    """Serializer for retrieving media files"""
    file_type = serializers.CharField(max_length=50, read_only=True)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ['id', 'title', 'description', 'file', 'uploaded_at', 'file_type','file_size', 'thumbnail', 'owner']
    
    def get_owner(self, obj):
        return obj.owner.username
