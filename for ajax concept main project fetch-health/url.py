"""
URL configuration for fetch_health project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from allauth.account.views import PasswordResetFromKeyDoneView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import TemplateView

from user.views import ProfileView, UpdateProfileImageView

from health_app.views import PdfFileDeleteView, PdfFileListView, PdfFileUploadView, chat_view ,ajax_view_get_method,ajax_view_post_method # isort: skip

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("pdf/", PdfFileListView.as_view(), name="pdf-list"),
   # path("chunk/", PdfChunkView.as_view(), name="pdf-chunk"),
    path("chunk/", ajax_view_get_method, name="pdf-chunk"),
    path("chunkstatus/", ajax_view_post_method, name="pdf-chunk-status"),
    path("upload/", PdfFileUploadView.as_view(), name="pdf-upload"),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html", post_reset_login=True),
        name="password_reset_confirm",
    ),
    path(
        "accounts/password/reset/key/done/",
        PasswordResetFromKeyDoneView.as_view(template_name="account/password_reset_from_key_done.html"),
        name="password_reset_from_key_done",
    ),
    path("pdf-delete/<int:pk>/", PdfFileDeleteView.as_view(), name="pdf-delete"),
    path("", TemplateView.as_view(template_name="index.html")),
    path("chat/", chat_view, name="chat"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path(
        "update-profile-image/",
        UpdateProfileImageView.as_view(),
        name="update-profile-image",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
