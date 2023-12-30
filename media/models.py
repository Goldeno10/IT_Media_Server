import os
import uuid
from io import BytesIO
from PIL import Image
from moviepy.editor import VideoFileClip

from django.conf import settings
from django.db import models
from django.utils.deconstruct import deconstructible
from django.core.files.base import ContentFile


@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        upload_to = os.path.join(self.path, str(instance.owner.id))
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(instance.id, ext)
        return os.path.join(upload_to, filename)


class Media(models.Model):
    """ A model for storing media files """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    file = models.FileField(upload_to=PathAndRename('media_files/'))
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50, blank=True, editable=False)
    file_size = models.CharField(max_length=50, blank=True, editable=False)

    def get_file_size(self):
        """Return the file size in a human-readable format"""
        size = self.file.size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size < 1024:
                return f'{size:.2f}{unit}'
            size /= 1024

    def generate_image_thumbnail(self):
        """ Generate thumbnail for image """
        if not self.thumbnail:
            # Open the original image
            original_image = Image.open(self.file.path)

            # Resize the image
            thumbnail_size = (300, 300)
            original_image.thumbnail(thumbnail_size)

            # Create a BytesIO buffer to save the image to memory
            thumbnail_buffer = BytesIO()

            # Save the thumbnail to the buffer in PNG format
            original_image.save(thumbnail_buffer, format='PNG')

            # Save the thumbnail to the database
            thumbnail_name = f'{self.id}_thumbnail.png'
            self.thumbnail.save(thumbnail_name, ContentFile(thumbnail_buffer.getvalue()), save=True)
    
    def generate_video_thumbnail(self):
        """ Generate thumbnail for video """
        if not self.thumbnail:
            # Generate thumbnail for video
            video = VideoFileClip(self.file.path)
            frame = video.get_frame(5)  # Get the frame at the 5th second
            video.close()

            # Create a BytesIO buffer to save the image to memory
            thumbnail_buffer = BytesIO()

            # Save the thumbnail to the buffer in PNG format
            Image.fromarray(frame).save(thumbnail_buffer, format='PNG')

            # Save the thumbnail to the 'thumbnails/' directory
            thumbnail_name = f'{self.id}_thumbnail.png'
            self.thumbnail.save(thumbnail_name, BytesIO(thumbnail_buffer.getvalue()), save=True)
    
    def generate_document_thumbnail(self):
        """ Generate thumbnail for document """
        if not self.thumbnail:
            # Note: You need to install PyMuPDF: pip install pymupdf
            import fitz

            pdf = fitz.open(self.file.path)
            page = pdf[0]  # Get the first page
            pix = page.get_pixmap()
            pdf.close()

            # Create a BytesIO buffer to save the image to memory
            thumbnail_buffer = BytesIO()

            # Save the thumbnail to the buffer in PNG format
            Image.frombytes('RGB', (pix.width, pix.height), pix.samples).save(thumbnail_buffer, format='PNG')

            # Save the thumbnail to the 'thumbnails/' directory
            thumbnail_name = f'{self.id}_thumbnail.png'
            self.thumbnail.save(thumbnail_name, BytesIO(thumbnail_buffer.getvalue()), save=True)
    
    def get_file_type(self):
        """ Return the type of the media file """
        file_type = self.file.name.split('.')[-1]
        if file_type in ['jpg', 'jpeg', 'png', 'gif']:
            return 'image'
        elif file_type in ['mp4', 'avi', 'mov', 'wmv']:
            return 'video'
        elif file_type in ['mp3', 'wav', 'ogg']:
            return 'audio'
        elif file_type in ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']:
            return 'document'
        else:
            return 'other'

    def save(self, *args, **kwargs):
        """ Override the save method to generate the thumbnail """
        super().save(*args, **kwargs)
        
        self.file_size = self.get_file_size()
        self.file_type = self.get_file_type()

        if self.file_type == 'image':
            self.generate_image_thumbnail()
        elif self.file_type == 'video':
            self.generate_video_thumbnail()
        elif self.file_type == 'document' and self.file.name.endswith('.pdf'):
            self.generate_document_thumbnail()
    
    def delete(self, *args, **kwargs):
        """ Override the delete method to delete the media file and the thumbnail """
        # Delete the thumbnail when the media file is deleted
        if self.thumbnail:
            thumbnail_path = self.thumbnail.path
            os.remove(thumbnail_path)

        # Delete the media file
        media_path = self.file.path
        os.remove(media_path)

        super().delete(*args, **kwargs)

    def __str__(self):
        """ Return the title of the media """
        return self.title
