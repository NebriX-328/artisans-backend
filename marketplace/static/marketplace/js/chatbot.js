document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("chatbot-btn");
  const popup = document.getElementById("chatbot-popup");
  const close = document.getElementById("chatbot-close");
  const sendBtn = document.getElementById("chatbot-send");
  const input = document.getElementById("chatbot-input");
  const messages = document.getElementById("chatbot-messages");

  // Toggle popup
  btn.addEventListener("click", () => {
    popup.style.display = popup.style.display === "flex" ? "none" : "flex";
  });

  close.addEventListener("click", () => {
    popup.style.display = "none";
  });

  // Send message
  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;

    // User message
    const userMsg = document.createElement("div");
    userMsg.textContent = msg;
    userMsg.style.cssText =
      "background:#ff9900;color:#fff;padding:6px 10px;border-radius:12px;margin:5px 0;text-align:right;";
    messages.appendChild(userMsg);

    // Bot response (simple echo for now)
    const botMsg = document.createElement("div");
    botMsg.textContent = "You said: " + msg;
    botMsg.style.cssText =
      "background:#eee;color:#333;padding:6px 10px;border-radius:12px;margin:5px 0;text-align:left;";
    messages.appendChild(botMsg);

    input.value = "";
    messages.scrollTop = messages.scrollHeight;
  }
});

document.querySelector(".chat-input button").addEventListener("click", async () => {
  const input = document.querySelector(".chat-input input");
  const query = input.value;
  input.value = "";

  const response = await fetch(`/ai_api/ai/?query=${query}&product=TestProduct&artisan=TestArtisan`);
  const data = await response.json();

  document.querySelector(".chat-messages").innerHTML += `
    <div class="message bot">
      <p><strong>Recommendations:</strong> ${data.recommendations}</p>
      <p><strong>DCA Code:</strong> ${data.dca_code}</p>
      <p><strong>Story:</strong> ${data.story}</p>
    </div>
  `;
});
