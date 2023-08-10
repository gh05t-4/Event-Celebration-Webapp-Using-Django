from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include('django.contrib.auth.urls')),
    path("addEvent/", views.addEvent, name="addEvent"),
    path("editEvent/<int:pk>/", views.editEvent, name="editEvent"),
    path("deleteEvent/<int:pk>/", views.deleteEvent, name="deleteEvent"),
    path("presentEvents/", views.presentEvents, name="presentEvents"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)