from django.shortcuts import render
from markdown2 import Markdown
from . import util
import random



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

# Make user input case insensitive
def validate(title):
    if title.capitalize() in util.list_entries():
        return title.capitalize()
    elif title.upper() in util.list_entries():
        return title.upper()
    else:
        return None

# Convert markdown to html format using Markdown library
def to_html(md):
    markdowner = Markdown()
    html = markdowner.convert(md)
    return html

# Displaying either of the error page or the entry page depending on the user's input
def entry(request, title):
    validation = validate(title)
    if validation == None:
        return render(request, "encyclopedia/error.html")
    else:
        entry = util.get_entry(validation)
        converted = to_html(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": validation,
            "converted": converted,
        })
            
def search(request):
    # Check if user's input is an entry or a sub-string of an entry
    entries = util.list_entries()
    if request.method == "POST":
        entry = request.POST['q']
        validation = validate(entry)
        if validation == None:
            choices = []
            for item in entries: 
                if entry.lower() in item.lower():
                    choices.append(item)
            # Return error if input is not even a sub-string of an entry, otherwise, return all entries containing that sub-string
            if len(choices) == 0:
                return render(request, "encyclopedia/error.html")
            else:
                return render(request, "encyclopedia/search.html", {
                    "choices": choices,
                    "input": entry
                })
                
        else:
            entry_content = util.get_entry(validation)
            converted = to_html(entry_content)
            return render(request, "encyclopedia/entry.html", {
                "title": entry,
                "converted": converted,
        })

def exist(title):
    entries = util.list_entries()
    for item in entries: 
            if title.lower() == item.lower():
                return True
                
def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        existing = exist(title)
        if existing:
            return render(request, "encyclopedia/error2.html")
        elif len(title) == 0:
            return render(request, "encyclopedia/error3.html", {
                "error_message": "Page title can't be empty"
            })

        else:
            util.save_entry(title, content)
            html = to_html(content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "converted": html,
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['page_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content,
    })

def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        edited = to_html(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "converted": edited,
    })

def random_page(request):
    entries = util.list_entries()
    choice = random.choice(entries)
    content = to_html(util.get_entry(choice))
    return render(request, "encyclopedia/entry.html", {
        "title": choice,
        "converted": content
    })