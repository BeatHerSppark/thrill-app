let docs = document.getElementsByClassName("grid-item");

const getRandColor = () => {
  const colors = ["#ffe5d9", "#ffcad4", "#d8e2dc"];

  return colors[Math.floor(Math.random() * 3)];
};

for (let i = 0; i < docs.length; i++) {
  docs[i].style.backgroundColor = getRandColor();
}
