from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def register(request: HttpRequest) -> HttpResponse:
    """Cadastra um usuário novo"""
    if request.method != "POST":
        # Exibe o formulário em branco de cadastro
        form = UserCreationForm()
    else:
        # Processa o formulário preenchido
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Faz o login do usuário e o redireciona para a página inicial
            login(request=request, user=new_user)
            return redirect("learning_logs:index")

    # Exibe um formulário em branco ou inválido
    context = {"form": form}
    return render(
        request=request, template_name="registration/register.html", context=context
    )
