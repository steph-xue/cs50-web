from django.shortcuts import render
from markdown2 import Markdown

from . import util


# Converts markdown content to html
def md_to_html(content):
    markdowner = Markdown()
    return markdowner.convert(content)
    

# Homepage with list of encyclopedia entries (in alphabetical order)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
