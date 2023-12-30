let docs = document.getElementsByClassName("grid-item");
const likeButton = document.getElementById("likeButton");

likeButton.addEventListener("click", () => {
  const user_id = likeButton.dataset.userId;
  const post_id = likeButton.dataset.postId;
  console.log(`${user_id} ${post_id}`);

  fetch("http://127.0.0.1:5000/api/like", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_id: user_id,
      post_id: post_id,
    }),
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error("gay");
      }
      return res.json();
    })
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.log(error);
    });
});

const getRandColor = () => {
  const colors = ["#ffe5d9", "#ffcad4", "#d8e2dc"];

  return colors[Math.floor(Math.random() * 3)];
};

for (let i = 0; i < docs.length; i++) {
  docs[i].style.backgroundColor = getRandColor();
}
