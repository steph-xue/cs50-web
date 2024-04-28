from django.shortcuts import render
import markdown

from . import util


# Converts markdown content to html
def md_to_html(md_content):
    markdowner = markdown.Markdown()
    return markdowner.convert(md_content)
    

# Displays the homepage with list of encyclopedia entries (in alphabetical order)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Displays the encyclopedia entry page for a specific title
def entry(request, title):
    md_content = util.get_entry(title)
    if md_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page not found"
        })
    else:
        html_content = md_to_html(md_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title, 
            "content": html_content
        })
