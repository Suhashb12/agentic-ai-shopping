/* ======================================================
   CHAT MESSAGE RENDERING (HTML SAFE)
====================================================== */

function addMessage(role, text, allowHTML = false) {
    const chatBox = document.getElementById("chat-box");

    const msg = document.createElement("div");
    msg.className = "message " + role;

    if (allowHTML) {
        msg.innerHTML = text;   // ✅ allow links
    } else {
        msg.textContent = text;
    }

    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;

    return msg;
}


/* ======================================================
   SEND MESSAGE (ASYNC)
====================================================== */

function sendMessage() {
    const input = document.getElementById("user-input");
    const text = input.value.trim();
    if (!text) return;

    // User message
    addMessage("user", text);
    input.value = "";

    // Thinking placeholder
    const thinkingMsg = addMessage("assistant", "thinking…");

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
    })
    .then(res => {
        if (!res.ok) throw new Error("Network error");
        return res.json();
    })
    .then(data => {
        thinkingMsg.remove();
        addMessage("assistant", data.reply, true); // ✅ allow HTML
    })
    .catch(err => {
        thinkingMsg.textContent = "Something went wrong. Please try again.";
        console.error(err);
    });
}


/* ======================================================
   ENTER KEY SUPPORT
====================================================== */

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("user-input");
    if (input) {
        input.addEventListener("keydown", e => {
            if (e.key === "Enter") sendMessage();
        });
    }
});


/* ======================================================
   PAYMENT LINK HANDLING
====================================================== */

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("payment-link")) {
        e.preventDefault();

        const url = e.target.href;
        const orderId = url.split("/").pop();

        // Open payment page
        window.open(url, "_blank");

        // Check order status after payment completes
        setTimeout(() => checkOrderStatus(orderId), 6000);
    }
});


/* ======================================================
   ORDER STATUS CHECK
====================================================== */

function checkOrderStatus(orderId) {
    fetch(`/api/order/${orderId}`)
        .then(res => res.json())
        .then(data => {
            if (data.status === "CONFIRMED") {
                addMessage(
                    "assistant",
                    `
                    ✅ <strong>Order Placed Successfully!</strong><br><br>
                    <b>🧾 Order ID:</b> ${orderId}<br>
                    <b>📦 Product:</b> ${data.product}<br>
                    <b>💰 Price:</b> ₹${data.price}<br>
                    <b>💳 Payment:</b> ${data.payment}<br>
                    <b>📍 Status:</b> ${data.status}
                    `,
                    true
                );
            }
        })
        .catch(err => console.error("Order check failed", err));
}


/* ======================================================
   PAYMENT PAGE → CHAT CALLBACK (OPTIONAL SUPPORT)
====================================================== */

window.addEventListener("message", function (event) {
    if (event.origin !== window.location.origin) return;

    if (event.data.type === "PAYMENT_SUCCESS") {
        checkOrderStatus(event.data.orderId);
    }
});


/* ======================================================
   AUTH MODAL (CHATGPT STYLE)
====================================================== */

function closeAuthModal() {
    const overlay = document.getElementById("auth-overlay");
    if (overlay) overlay.classList.add("hidden");
}

// Show signup/login modal after delay (guest only)
setTimeout(() => {
    const loggedIn = document.body.dataset.loggedin;
    const overlay = document.getElementById("auth-overlay");

    if (!loggedIn && overlay) {
        overlay.classList.remove("hidden");
    }
}, 2000);
