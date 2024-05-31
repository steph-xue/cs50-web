// Allows retrieval of cookies
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


// Allows the user to add or remove a like from a post
function like_handler(id) {

    // Get the like button so we can eventually change it
    const btn = document.getElementById(`${id}`);

    // Using an API, check the user's like status of the post
    fetch(`/like_status/${id}`)
    .then(response => response.json())
    .then(result => {

        // Get the user's like status of the post
        let liked = result["liked"];

        // If the post has not yet been liked, like the post
        if (!liked) {

            // Using an API, change the post to add a like and save it to the database
            fetch(`/add_like/${id}`)
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
    })
}

