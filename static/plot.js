function checkNum() {
  const inputNum = document.querySelector("#inputData");
  // console.log(inputNum);
  boolNum = !isNaN(parseFloat(inputNum.value)) && isFinite(inputNum.value);
  if (!boolNum) {
    document.querySelector("input[type=submit]").disabled = true;
    inputNum.parentElement.appendChild(document.createElement("p"));
    document.querySelector("p").innerHTML = "格式错误";
    document.querySelector("p").className = "formatError";
  } else {
    document.querySelector("input[type=submit]").disabled = false;
    if (document.querySelector("p") != null) {
      document
        .querySelector("p")
        .parentElement.removeChild(document.querySelector("p"));
      inputNum.className = "";
    }
  }
}

function plot() {
  const submit = document.querySelector("input[type=submit]");
  const embed = document.querySelector("embed");
  submit.onclick = function () {
    embed.src = "../static/image.svg";
  };
}
