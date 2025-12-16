function addMessage(role, text) {
  const box = document.getElementById("chat-box");
  const div = document.createElement("div");
  div.className = "message " + role;
  div.textContent = text;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById("user-input");
  const msg = input.value.trim();
  if (!msg) return;

  addMessage("user", msg);
  input.value = "";

  addMessage("assistant", "thinking...");

  fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: msg})
  })
  .then(res => res.json())
  .then(data => {
    document.querySelector(".assistant:last-child").textContent = data.reply;
  });
}
