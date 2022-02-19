from django import contrib
from django.core.checks import messages
from django.forms.widgets import FileInput
from django.shortcuts import redirect, render
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia

#Dashboard

def home(request):
    return render(request, 'dashboard/home.html')


# Notes Card

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
            messages.success(
            request, f"Notes Added from {request.user.username} Successfully!")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)


def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes


# Homework Card

def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                deadline=request.POST['deadline'],
                is_finished=finished,
            )
            homeworks.save()
            messages.success(
                request, f'Homework Added from {request.user.username}!!')
    else:
        form = HomeworkForm()
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    context = {'homeworks': homework,
               'homework_done': homework_done,
               'form': form,
               }
    return render(request, 'dashboard/homework.html', context)


def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


# YouTube Card

def youtube(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=25)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list,
            }
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashboardFom()
    context = {'form': form}
    return render(request, "dashboard/youtube.html", context)


# ToDo Card

def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
            messages.success(request, f"Todo Added from {request.user.username}!!")
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form':form,
        'todos': todo,
        'todos_done': todos_done
    }
    return render(request, "dashboard/todo.html", context)

def update_todo(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect(todo)
    
    
#Books Card

def books(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {               
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),                           
            }            
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list,
            }
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashboardFom()
    context = {'form': form}
    return render(request, "dashboard/books.html", context)


#Dictionary Card

def dictionary(request):
    if request.method == "POST":
        form = DashboardFom(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text        
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text'] 
            audio = answer[0]['phonetics'][0]['audio']
            defintion = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'defintion':defintion,
                'example':example,
                'synonyms':synonyms,
            }            
        except:
            context = {
                'form':form,
                'input':'',
            }                      
        return render(request,"dashboard/dictionary.html",context)
    else:
        form = DashboardFom()
        context = {'form':form}
    return render(request, "dashboard/dictionary.html",context)


#Wiki Card

def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardFom(request.POST)
        search = wikipedia.page(text)
        context = {
            'form':form,
            'title':search.title,
            'limk':search.link,
            'details':search.summary
        }
    form = DashboardFom()
    context = {
        'form':form
    }
    return render(request, "dashboard/wiki.html",context)