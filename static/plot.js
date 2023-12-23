function plot() {
  const button = document.querySelector("input[type=button]");
  const embed = document.querySelector("embed");
  button.onclick = function () {
    embed.src = "../static/image.svg";
  };
}
