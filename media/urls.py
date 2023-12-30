from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    HomePage, MediaDetailView,
    UploadMediaView, UpdateMediaView,
    DeleteMediaView,
    MediaViewSet
)

router = DefaultRouter()
router.register('api', MediaViewSet, basename='api')

app_name = 'media'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('media/<uuid:pk>/', MediaDetailView.as_view(), name='detail'),
    path('upload/', UploadMediaView.as_view(), name='upload'),
    path('update/<uuid:pk>', UpdateMediaView.as_view(), name='media_update'),
    path('delete/<uuid:pk>', DeleteMediaView.as_view(), name='media_delete'),
]

urlpatterns += router.urls
