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


// Allows the user to like or remove a like from a post
function like_handler(id, your_liked_post_ids) {

    // Get the like button to change and clear it out
    const btn = document.querySelector(`#${id}`);
    btn.innerHTML = "";

    // Checks if the user has liked the post
    if (your_liked_post_ids.indexOf < 0) {
        let liked = false;
    } else {
        let liked = true;
    }

    // If the post has not yet been liked, like the post
    if (liked == false) {

        // Using an API, change the post to add a like and save it to the database
        fetch(`/like/${id}`)
        .then(response => response.json())
        .then(result => {

            // Prints the results (if adding the like was successful) to the console
            console.log(result);
            btn.innerHTML = " Remove Like";
        })
    
    // If the post has already been liked, remove the like from the post
    } else {
        // Using an API, change the post to remove the like and save it to the database
        fetch(`/remove_like/${id}`)
        .then(response => response.json())
        .then(result => {

            // Prints the results (if removing the like was successful) to the console
            console.log(result);
            btn.innerHTML = " Like";
        })
    }

    // After adding/removing the like, change the variable liked accordingly
    liked = !liked
    
}


