const chatMessages = document.getElementById("chat-messages");
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

// scroll helper
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// auto resize
function autoResize() {
    userInput.style.height = 'auto';
    const newHeight = Math.min(userInput.scrollHeight, 200);
    userInput.style.height = newHeight + 'px';
}
userInput.addEventListener('input', autoResize);

// buat pesan
function addMessage(content, isUser = false) {
    const messageGroup = document.createElement("div");
    messageGroup.className = `message-group ${isUser ? "user-group" : "bot-group"} fade-in`;

    const message = document.createElement("div");
    message.className = `message ${isUser ? "user-message" : "bot-message"}`;

    const text = document.createElement("span");
    text.className = "message-text";
    text.innerHTML = content;

    const time = document.createElement("span");
    time.className = "message-time";
    time.textContent = new Date().toLocaleTimeString("id-ID", { hour: "2-digit", minute: "2-digit" });

    message.appendChild(text);
    message.appendChild(time);
    messageGroup.appendChild(message);
    chatMessages.appendChild(messageGroup);

    autoResize()
    scrollToBottom();
}

// typing indicator
function showTyping() {
    const typing = document.createElement("div");
    typing.className = "message-group bot-group fade-in";
    typing.id = "typing-indicator";
    typing.innerHTML = `
        <div class="typing-indicator">
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(typing);
    scrollToBottom();
    autoResize()
}

function hideTyping() {
    const typing = document.getElementById("typing-indicator");
    if (typing) typing.remove();
}

// disable/enable input
function disableInput() {
    userInput.disabled = true;
    sendButton.disabled = true;
}

function enableInput() {
    userInput.disabled = false;
    sendButton.disabled = false;
    userInput.focus();
}

// handle submit
async function handleSubmit(e) {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // tampilkan pesan user
    addMessage(message, true);

    // clear input + disable
    userInput.value = "";
    disableInput();

    // fake typing
    showTyping();

    try {
        const response = await fetch("/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });
        const data = await response.json();

        hideTyping();
        if (data.status === "success") {
            addMessage(data.response);
        } else {
            addMessage("⚠️ Terjadi kesalahan: " + (data.message || "Tidak diketahui"));
        }
    } catch (err) {
        console.error("Error:", err);
        hideTyping();
        addMessage("⚠️ Gagal komunikasi dengan server");
    } finally {
        enableInput();
    }
}

// Enter untuk submit
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit(e);
    }
});

// kirim form
chatForm.addEventListener("submit", handleSubmit);

// auto scroll saat load
scrollToBottom();

// auto resize userInput
autoResize();