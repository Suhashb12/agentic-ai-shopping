/* ===============================
   CHAT MESSAGE HELPERS
================================ */

function addMessage(role, text) {
  const chatBox = document.getElementById("chat-box");

  const msg = document.createElement("div");
  msg.className = "message " + role;
  msg.textContent = text;

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;

  return msg;
}


/* ===============================
   SEND MESSAGE (ASYNC)
================================ */

function sendMessage() {
  const input = document.getElementById("user-input");
  const text = input.value.trim();
  if (!text) return;

  // Show user message immediately
  addMessage("user", text);
  input.value = "";

  // Show thinking placeholder
  const thinkingMsg = addMessage("assistant", "thinking…");

  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: text })
  })
  .then(res => {
    if (!res.ok) {
      throw new Error("Network response was not ok");
    }
    return res.json();
  })
  .then(data => {
    thinkingMsg.textContent = data.reply;
  })
  .catch(err => {
    thinkingMsg.textContent = "Something went wrong. Please try again.";
    console.error(err);
  });
}


/* ===============================
   ENTER KEY SUPPORT
================================ */

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("user-input");
  if (input) {
    input.addEventListener("keydown", e => {
      if (e.key === "Enter") {
        sendMessage();
      }
    });
  }
});


/* ===============================
   AUTH MODAL (CHATGPT STYLE)
================================ */

function closeAuthModal() {
  const overlay = document.getElementById("auth-overlay");
  if (overlay) {
    overlay.classList.add("hidden");
  }
}

// Show modal after delay ONLY for guest users
setTimeout(() => {
  const loggedIn = document.body.dataset.loggedin;
  const overlay = document.getElementById("auth-overlay");

  if (!loggedIn && overlay) {
    overlay.classList.remove("hidden");
  }
}, 2000);
