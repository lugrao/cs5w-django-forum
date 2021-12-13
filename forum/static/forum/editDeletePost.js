let editButtons = document.querySelectorAll(".edit-button")
let deleteButtons = document.querySelectorAll(".delete-button")

editButtons.forEach((button) => {
  button.onclick = function () {
    editPost(this)
  }
})

deleteButtons.forEach((button) => {
  button.onclick = function () {
    deletePost(this)
  }
})

function editPost(button) {
  let id = button.dataset.id
  let saveButton = document.querySelector(`#post-${id} .save-button`)
  let cancelButton = document.querySelector(`#post-${id} .cancel-button`)
  let deleteButton = document.querySelector(`#post-${id} .delete-button`)
  let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value
  let postContent = document.querySelector(`#post-${id} .post-content`)
  let previousPost = postContent.innerText

  // Show Textarea
  postContent.innerHTML = `<textarea style="width:100%;" cols="50" rows="3">${postContent.innerText}</textarea>`

  // Hide Edit button
  button.classList.add("hidden")

  // Hide Delete button
  deleteButton.classList.add("hidden")

  // Show Save button
  saveButton.classList.remove("hidden")

  // Show Cancel button
  cancelButton.classList.remove("hidden")

  // Save edited post
  saveButton.onclick = () => {
    let editedPostContent = postContent.firstChild.value
    let data = new FormData()
    data.append("id", id)
    data.append("post-content", editedPostContent)
    data.append("csrfmiddlewaretoken", csrfToken)

    if (editedPostContent) {
      fetch(`/edit-post/${id}`, {
        method: "POST",
        body: data,
        credentials: "same-origin",
      })
        .then((res) => res.json())
        .then((result) => {
          console.log(result)
        })
        .catch((error) => {
          console.log(error)
        })

      // Update postContent element
      postContent.innerHTML = editedPostContent
    } else {
      // Restore previous post
      postContent.innerHTML = previousPost
    }

    // Show Edit button
    button.classList.remove("hidden")

    // Show Delete button
    deleteButton.classList.remove("hidden")

    // Hide Save button
    saveButton.classList.add("hidden")

    // Hide Cancel button
    cancelButton.classList.add("hidden")
  }

  // Handle cancel
  cancelButton.onclick = () => {
    console.log("CLIECKS")
    postContent.innerHTML = previousPost
    // Show Edit button
    button.classList.remove("hidden")

    // Show Delete button
    deleteButton.classList.remove("hidden")

    // Hide Save button
    saveButton.classList.add("hidden")

    // Hide Cancel button
    cancelButton.classList.add("hidden")
  }
}

function deletePost(button) {
  let id = button.dataset.id
  let post = document.querySelector(`#post-${id}`)
  let comments = document.querySelector("#comments")
  let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value
  let data = new FormData()
  data.append("id", id)
  data.append("csrfmiddlewaretoken", csrfToken)

  fetch(`/delete-post/${id}`, {
    method: "POST",
    body: data,
    credentials: "same-origin",
  })
    .then((res) => res.json())
    .then((result) => {
      console.log(result)
    })
    .catch((error) => {
      console.log(error)
    })

  // Hide post
  post.classList.add("hidden")

  // Hide comments and show message
  if (comments) {
    comments.classList.add("hidden")
    document.querySelector(
      ".body"
    ).innerHTML = `<p class="message">Post deleted.</p>`
  }
}
