from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from . import forms
from random import randrange

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, TITLE):
    if util.get_entry(TITLE):
        return render(request, "encyclopedia/entries.html", {
            "content": util.get_entry(TITLE),
            "title": TITLE
        })
    else:
        return render(request, "encyclopedia/entries.html", {
            "content": TITLE + " does not exist"
        })
    
def search(request):
    query = request.GET.__getitem__('q')
    search_results = []
    for entry in util.list_entries():
            if query in entry:
                search_results.append(entry)

    if query in util.list_entries():
        return render(request, "encyclopedia/entries.html", {
            "content": util.get_entry(query)
        })
    else:
        if search_results:
            return render(request, "encyclopedia/search.html", {
                "search_results": search_results,
                "query": query
            })
        else:
            return render(request, "encyclopedia/search.html", {
                "error": 'Sorry nothing found,try again?',
                "query": query
            })

def new(request):
    if request.method == "POST":
        form = forms.PageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["content"]
            status = request.POST.__getitem__('status')
            if title in util.list_entries() and status != 'edit' :
                return render(request, "encyclopedia/create_page.html", {
                    "form": form,
                    "error": "Your Title already exists!!",
                })    
            util.save_entry(title,entry)
            return HttpResponseRedirect(reverse('wiki', args=[title]))
        else:
            return render(request, "encyclopedia/create_page.html", {
                "form": form,
                "error": "Check your inputs.",
            })
    elif request.method == 'GET' and request.GET.get('status', None):
        form = forms.PageForm(request.GET)
        status= request.GET.get('status','create')
        return render(request, "encyclopedia/create_page.html" ,{
            "form": form,
            "status": status
        })
    
    return render(request, "encyclopedia/create_page.html", {
        'form':forms.PageForm(),
    })

def random(request):
    title = util.list_entries()[randrange(len(util.list_entries()))]
    return render(request, "encyclopedia/entries.html", {
        'content': util.get_entry(title)
    })
