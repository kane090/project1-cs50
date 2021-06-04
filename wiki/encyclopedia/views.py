from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from markdown2 import markdown
from django.urls import reverse
from random import randrange

from . import util


def index(request):
    page_name = request.GET.get('q')
    if page_name != None:
        return search(request, page_name)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def entry(request, page_name):
    try:
        return render(request, "encyclopedia/entry.html", {
            "title": page_name,
            "entry": markdown(util.get_entry(page_name))
        })
    except TypeError:
        return render(request, "encyclopedia/error.html")

def search(request, page_name):
    subset_entries = []
    og_entries_list = util.list_entries()
    entries_list = [entry.lower() for entry in og_entries_list]
    if (page_name in entries_list) or (page_name in og_entries_list):
        return entry(request, page_name)
    else:
        for i in range(len(entries_list)):
            if page_name in entries_list[i]:
                subset_entries.append(og_entries_list[i])
        return render(request, "encyclopedia/search_results.html", {
            "entries": subset_entries
        })

def new_entry(request):
    current_entries = [entry.lower() for entry in util.list_entries()]
    title = request.POST.get('title')
    content = request.POST.get('markdown')
    if title != None:
        lower_title = title.lower()
        if lower_title in current_entries:
            return render(request, "encyclopedia/error_alreadyexists.html")
        else:
            content = content.replace("\r", "")
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        return render(request, "encyclopedia/new.html")

def edit_entry(request, page_name):
    content = util.get_entry(page_name)
    new_content = request.POST.get('markdown')
    if new_content != None:
        new_content = new_content.replace("\r", "")
        util.save_entry(page_name, new_content)
        return HttpResponseRedirect(reverse("entry", args=[page_name]))
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": page_name,
            "content": content
        })

def random_page(request):
    current_entries = util.list_entries()
    index = randrange(0, len(current_entries))
    return HttpResponseRedirect(reverse("entry", args=[current_entries[index]]))
