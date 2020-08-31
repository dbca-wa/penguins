from __future__ import absolute_import
from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

from observations.sites import site
from observations.api import PenguinCountViewSet, PenguinObservationViewSet, VideoViewSet
from observations.views import VideoImport, S3View


router = DefaultRouter()
router.register(r'count', PenguinCountViewSet)
router.register(r'observations', PenguinObservationViewSet)
router.register(r'videos', VideoViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^markitup/', include('markitup.urls')),
    url(r'^help/', include('django.contrib.flatpages.urls')),
    #url(r'^cronjobs/video-import/$', VideoImport.as_view(), name='cronjobs_video_import'),
    url(r'^observations/s3/$', S3View.as_view(), name='s3_view'),
    url(r'', include(site.urls)),
)
