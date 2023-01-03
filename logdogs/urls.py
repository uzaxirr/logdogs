from django.contrib import admin
from django.urls import include, path

from watcher.views import ListenEventView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("generator.urls")),
    path("listen/<uuid:source_uuid>",
         ListenEventView.as_view(), name="listen_events"),
]
