from django.shortcuts import render, redirect
from .models import Todo
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def index(request):
    todos = Todo.objects.filter(is_done=False)
    done_todos = Todo.objects.filter(is_done=True)
    return render(request, 'todoListApp/todoList.html', {'todos': todos, 'done_todos': done_todos})

def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(title=title)
    return redirect('todoListApp:index')

def mark_done(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(Todo, id=todo_id)
        todo.is_done = True
        todo.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def delete_todo(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(Todo, id=todo_id)
        todo.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})