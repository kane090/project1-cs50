from django.shortcuts import render
from markdown2 import markdown

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
            "title": page_name.capitalize(),
            "entry": markdown(util.get_entry(page_name))
    })
    except TypeError:
        return render(request, "encyclopedia/error.html")

def search(request, page_name):
    subset_entries = []
    og_entries_list = util.list_entries()
    entries_list = [entry.lower() for entry in og_entries_list]
    if page_name in entries_list:
        return entry(request, page_name)
    else:
        for i in entries_list:
            if page_name in i:
                subset_entries.append(i)
        return render(request, "encyclopedia/search_results.html", {
            "entries": subset_entries
        })
