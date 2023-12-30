import mimetypes

from django.http import FileResponse, HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import  FormView
from django.shortcuts import redirect
from django.contrib.auth import logout

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView

from .forms import MediaUploadForm, MediaUpdateForm
from .utils import categorize_file
from .models import Media
from .serializers import MediaSerializer, RetrieveMediaSerializer
from .forms import MediaUploadForm


class MediaViewSet(viewsets.ModelViewSet):
    """API endpoint for listing and creating media files"""
    queryset = Media.objects.all()

    def create(self, request, *args, **kwargs):
        """Create a media file and categorize it based on its type"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """Save a media file, categorize it based on its type, and generate a thumbnail"""
        file_instance = serializer.save(owner=self.request.user)
        file_path = file_instance.file.path
        file_instance.file_type = categorize_file(file_path)
        file_instance.save()


    def retrieve(self, request, *args, **kwargs):
        """Retrieve a media file and return it as a response"""
        instance = self.get_object()
        file_path = instance.file.path
        content_type, _ = mimetypes.guess_type(file_path)

        # If the file is a video, audio, image, or document, return it as a FileResponse
        if instance.file_type in ['video', 'audio', 'image', 'document']:
            response = FileResponse(open(file_path, 'rb'), content_type=content_type)
            return response
        elif instance.file_type in ['image', 'document']:
            response = HttpResponse(open(file_path, 'rb'), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{instance.file.name}"'
            return response
        else:
            return super().retrieve(request, *args, **kwargs)
    
    def get_serializer_class(self):
        """Return the appropriate serializer class based on the action"""
        if self.request.method == 'POST':
            return MediaSerializer
        else:
            return RetrieveMediaSerializer


class HomePage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """ Add the media objects and upload form to the context"""
        context = super().get_context_data(**kwargs)
        context['media_objects'] = Media.objects.all()
        context['media_update_form'] = MediaUpdateForm()

        return context


class MediaDetailView(TemplateView):
    """Display the details of a media object"""
    template_name = 'media_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['media'] = Media.objects.get(id=self.kwargs['pk'])

        return context


class UploadMediaView(FormView):
    """ Display a form for uploading media files """
    template_name = 'upload_media.html'
    form_class = MediaUploadForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload_form'] = self.get_form()
        return context


class DeleteMediaView(APIView):
    """ Delete a media object """
    def get(self, request, pk):
        media = Media.objects.get(pk=pk)
        if media:
            media.delete()        
        return redirect('media:home')


class UpdateMediaView(APIView):
    """ Update a media object """
    def post(self, request, pk):
        media = Media.objects.get(pk=pk)
        if media:
            form = MediaUpdateForm(request.POST, instance=media)
            if form.is_valid():
                form.save()
                return redirect('media:home')
        return redirect('media:home')
    
