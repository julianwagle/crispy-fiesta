from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from {{cookiecutter.project_slug}}.drf_auth.views import ( 
    PasswordResetView,
    PasswordResetConfirmView,
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView
)
from {{cookiecutter.project_slug}}.drf_auth.registration.views import (
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView
)

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("{{ cookiecutter.project_slug }}.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),

    # Your stuff: custom urls includes go here

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
# ==========================================
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token),

    # URLs that do not require a session or valid token
    path('api/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('api/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('api/users/login/', LoginView.as_view(), name='rest_login'),
    # # URLs that require a user to be logged in with a valid session / token.
    path('api/logout/', LogoutView.as_view(), name='rest_logout'),
    path('api/user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('api/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),

    # URLs with views located in rest_auth/registration
    path('api/users/', RegisterView.as_view(), name='rest_register'),
    path('api/resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path('api/confirm-email/<key>/', VerifyEmailView.as_view(), name='email_verification_sent'),


]

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
