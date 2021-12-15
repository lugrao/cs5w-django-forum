let likeButtons = document.querySelectorAll(".like-button")

likeButtons.forEach((button) => {
  button.onclick = function () {
    like(this)
  }
})

function like(button) {
  let id = button.dataset.id
  let liked = button.dataset.liked
  let likes = parseInt(button.dataset.likes)
  let likedObject = button.dataset.likedobject
  let csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value
  let data = new FormData()
  data.append("id", id)
  data.append("liked_object", likedObject)
  data.append("csrfmiddlewaretoken", csrfToken)

  fetch(`/like/${liked}`, {
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

  if (liked == "True") {
    button.dataset.liked = "False"
    button.dataset.likes = likes - 1
    button.innerText = "🤍"
  } else if (liked == "False") {
    button.dataset.liked = "True"
    button.dataset.likes = likes + 1
    button.innerText = "❤️"
  }
  document.querySelector(`#${likedObject}-${id} .like-number`).innerText = button.dataset.likes
}
