from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.text import slugify
from django.urls import reverse

from tasks.models import Collection, Task


# Create your views here.
def index(request):
    context = {}
    collection_slug = request.GET.get("collection")
    #collection=Collection.get_default_collection()
    if collection_slug == None:
        Collection.get_default_collection()
        return redirect(f"{reverse('home')}?collection=_defaut")

    collection= get_object_or_404(Collection, slug=collection_slug)

    collections=Collection.objects.order_by('slug')
    context["collections"]=collections
    tasks=collection.task_set.order_by("description")
    context["tasks"]=tasks
    context["collection"]=collection 
    #context["tasks"]=render_to_string('tasks/tasks.html', context={"tasks":tasks})
    return render(request, 'tasks/index.html',context)


def add_collection(request):
    context={}
    collection_name=escape(request.POST.get("collection-name"))
    collection, created=Collection.objects.get_or_create(name=collection_name,slug=slugify(collection_name))
    if not created:
        return HttpResponse("La collection existe déjà", status=409)
    context["collection"]=collection
    return render(request, 'tasks/collections.html',context=context)

def add_task(request):
    print(request.POST)
    collection=Collection.objects.get(slug=request.POST.get("collection"))
    description=escape(request.POST.get("task-description"))
    task=Task.objects.create(description=description, collection=collection)

    return render(request, 'tasks/task.html', context={'task':task})

def delete_task(request, task_pk):
    task= get_object_or_404(Task, pk=task_pk)
    task.delete()
    return HttpResponse("")

def delete_collection(request, collection_pk):
    collection=get_object_or_404(Collection, pk=collection_pk)
    collection.delete()
    return redirect('home')


def get_task(request,collection_pk):
    context={}
    collection=get_object_or_404(Collection,pk=collection_pk)
    tasks=collection.task_set.order_by("description")
    context["tasks"]=tasks
    context["collection"]=collection
    return render(request,'tasks/tasks.html', context=context )