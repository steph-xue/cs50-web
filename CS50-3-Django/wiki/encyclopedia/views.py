from django.shortcuts import render
import markdown
import os
import random

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

    # If entry page does not exist, displays an error message
    if md_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page not found"
        })
    # If entry page exists, displays the entry's page
    else:
        html_content = md_to_html(md_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title, 
            "content": html_content
        })


# Displays the encyclopedia entry page or search results page for the user's search
def search(request):

    # Gets list of all entries & the user's search
    entrylist = util.list_entries()
    search = request.POST["q"]

    # Displays the encyclopedia entry page if the search result matches a valid entry
    if util.get_entry(search) is not None:
        md_content = util.get_entry(search)
        html_content = md_to_html(md_content)
        return render(request, "encyclopedia/entry.html", {
            "title": search,
            "content": html_content
        })
    # Otherwise displays the search results page with a list of entries that match the query as a substring
    else:
        validentries = []
        for entry in entrylist:
            if search.lower() in entry.lower():
                validentries.append(entry)
        return render(request, "encyclopedia/search.html", {
                "entries": validentries
            })
    

# Allows the user to create a new entry page
def create(request):

    # POST -  User submits the form (title and content) to create a new entry page
    if request.method == "POST":

        # Gets list of all current entries & the user's title and content for the new entry page
        entrylist = util.list_entries()
        title = request.POST["title"].capitalize()
        md_content = request.POST["content"]

        # If entry already exists, displays an error message
        if title in entrylist:
            return render(request, "encyclopedia/error.html", {
            "message": "Entry already exists"
        })
        # If entry does not exist, saves the entry and redirects user to the new entry's page
        else:
            util.save_entry(title, md_content)
            html_content = md_to_html(md_content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })

    # GET - User reaches the create a new entry page
    else:
        return render(request, "encyclopedia/create.html")
    

# Allows the user start edits for an entry page 
def edit(request):

    # POST - Takes the user's request to edit a specific entry title to render the edit page
    if request.method == "POST":
        title = request.POST["title"]
        md_content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": md_content
        })
    

# Allows the user to save edits for an entry page
def save_edit(request):
    
    # POST - Saves the edits made to the title and content for a specific entry page
    if request.method == "POST":
        title = request.POST["title"]
        md_content = request.POST["content"]
        util.save_entry(title, md_content)
        html_content = md_to_html(md_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


# Allows the user delete an entry page 
def delete(request):

    # POST - Takes the user's request to delete a specific entry title 
    if request.method == "POST":

        # Gets title of entry to delete
        title = request.POST["title"]

        # Deletes the entry file
        os.remove(f"entries/{title}.md")
        
        # Returns the user to the homepage
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })
    

# Displays a random entry page to the user
def randomchoice(request):

    # Gets the list of all entries and selects a random one
    entrylist = util.list_entries()
    entry = random.choice(entrylist)

    # Displays the title and contents of the random entry to the user
    md_content = util.get_entry(entry)
    html_content = md_to_html(md_content)
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "content": html_content
    })
        




    
    
    



