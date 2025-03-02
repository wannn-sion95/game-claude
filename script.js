function sendCommand() {
  let inputField = document.getElementById("command-input");
  let outputDiv = document.getElementById("game-output");
  let command = inputField.value.trim();

  if (command === "") return;

  fetch("/command", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ command: command }),
  })
    .then((response) => response.json())
    .then((data) => {
      outputDiv.innerHTML += "<p>> " + command + "</p>";
      outputDiv.innerHTML += "<p>" + data.response + "</p>";
      inputField.value = "";
      outputDiv.scrollTop = outputDiv.scrollHeight;
    })
    .catch((error) => console.error("Error:", error));
}
