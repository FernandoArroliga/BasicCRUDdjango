from django.shortcuts import render, redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Tarea

from .forms import TareaForm

# Create your views here.
def home(request):
    """
    tareas = Tarea.objects.all()
    context = {'tareas': tareas}
    return render(request, 'todo/home.html', context)
    """

    tareas_list = Tarea.objects.all()
    paginator = Paginator(tareas_list, 4)  # Show 4 items per page

    page = request.GET.get('page')
    try:
        tareas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        tareas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page.
        tareas = paginator.page(paginator.num_pages)

    context = {'tareas': tareas}
    return render(request, 'todo/home.html', context)


def agregar(request):

    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TareaForm()
    context = {'form': form}
    return render(request, 'todo/agregar.html', context)

def eliminar(request, tarea_id):
    tarea = Tarea.objects.get(id=tarea_id)
    tarea.delete()
    return redirect('home')

def editar(request, tarea_id):
    tarea = Tarea.objects.get(id=tarea_id)
    
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TareaForm(instance=tarea)

    context = {'form': form}
    return render(request, 'todo/editar.html', context)