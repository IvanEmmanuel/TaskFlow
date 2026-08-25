"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.tasks import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include("apps.tasks.urls")),
    
    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"), 
                                    # ¿Qué hace redirect_authenticated_user=True?
    # Si el usuario ya está autenticado y trata de entrar a /login/, 
    # no le muestres el formulario de login; redirígelo directamente al destino de usuarios autenticados.
    # en settings.py -> LOGIN_REDIRECT_URL = "/tasks/"
    
    
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name = "registration/password_reset.html"
        ), 
         name="password_reset",
    ),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name= "registration/password_reset_done.html"
        ),
         name="password_reset_done",
    ),
    path("password-reset/confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name = "registration/password_reset_confirm.html"
        ),
         name="password_reset_confirm",
    ),
    path("password-reset/complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name = "registration/password_reset_complete.html"
        ),
         name="password_reset_complete",
    ),
    
    ###############################################
    ######          URLs de la API
    ###############################################
    
    path("api/", include("apps.tasks.api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # OpenAPI
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    # Swagger
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),
]
