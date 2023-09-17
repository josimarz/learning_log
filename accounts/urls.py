"""Define padrões de URL para contas"""

from django.urls import include, path

from . import views

app_name = "accounts"
urlpatterns = [
    # Inclui URLs de autenticação default
    path("", include("django.contrib.auth.urls")),
    # Página de cadastro
    path("register/", views.register, name="register"),
]
