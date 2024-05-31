// When the web application loads, loads the entire document before handling any events
document.addEventListener('DOMContentLoaded', function() {

});


// Allows to retrieve cookies
function get_cookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) return parts.pop().split(';').shift();
}


// Allows the user to edit a post
function edit(id) {

    // Gets the content of the post with a specific id 
    const content = document.querySelector(`#post_content_${id}`).value

    // Using an API, posts the content to the backend to save the edit to the database
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": get_cookie("csrftoken")},
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(result => {

        // Prints the results (if the edit was successful) to the console
        console.log(result);

        // Directed modifies the content of the post to reflect the edits (without needing to refresh)
        document.querySelector(`#content_${id}`).innerHTML = result["data"]
    })
}


