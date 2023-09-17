from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import EntryForm, TopicForm
from .models import Entry, Topic


def index(request: HttpRequest) -> HttpResponse:
    """A página inicial para o Registro de Aprendizagem"""
    return render(request=request, template_name="learning_logs/index.html")


@login_required
def topics(request: HttpRequest) -> HttpResponse:
    """Mostra todos os tópicos"""
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}
    return render(
        request=request, template_name="learning_logs/topics.html", context=context
    )


@login_required
def topic(request: HttpRequest, topic_id: int) -> HttpResponse:
    """Mostra um único tópico e todas as suas entradas"""
    topic = Topic.objects.get(id=topic_id)
    # Verifica se o tópico pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by("-date_added")
    context = {"topic": topic, "entries": entries}
    return render(
        request=request, template_name="learning_logs/topic.html", context=context
    )


@login_required
def new_topic(request: HttpRequest) -> HttpResponse:
    """Adiciona um tópico novo"""
    if request.method != "POST":
        # Nenhum data enviado; cria um formulário em branco
        form = TopicForm()
    else:
        # Dados POST enviados; processa os dados
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topics")
    # Exibe um formulário em branco ou inválido
    context = {"form": form}
    return render(
        request=request, template_name="learning_logs/new_topic.html", context=context
    )


@login_required
def new_entry(request: HttpRequest, topic_id: int) -> HttpResponse:
    """Adiciona uma entrada nova para um tópico específico"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != "POST":
        # Nenhum dado enviado; cria um formulário em branco
        form = EntryForm()
    else:
        # Dados POST enviados; processa os dados
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    # Exibe o formulário em branco ou inválido
    context = {"topic": topic, "form": form}
    return render(
        request=request, template_name="learning_logs/new_entry.html", context=context
    )


@login_required
def edit_entry(request: HttpRequest, entry_id: int) -> HttpResponse:
    """Edita uma entrada existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != "POST":
        # Requisição inicial; pré-preenche formulário com a entrada atual
        form = EntryForm(instance=entry)
    else:
        # Dados POST enviados; processa os dados
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(
        request=request, template_name="learning_logs/edit_entry.html", context=context
    )
