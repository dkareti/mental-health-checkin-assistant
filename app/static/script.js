async function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value;

  // seperate the chat
  const messageHist = document.getElementById("messageHistory");

  if (!message) return; // Don't send empty messages

  input.value = "";

  // Display user's message
  messageHist.innerHTML += `<p class='user'><b>Your Message:</b> ${message}</p>`;

  try {
    // Send message to the server (backend endpoint)
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    // Display bot's reply
    const botMsg = document.createElement("p");
    botMsg.className = "bot";
    const botLabel = document.createElement("b");
    botLabel.textContent = "Wellness Assistant: ";
    botMsg.appendChild(botLabel);
    botMsg.appendChild(document.createTextNode(data.reply));  // No \ issues here
    messageHist.appendChild(botMsg);

  } catch (error) {
    console.error("Error sending message:", error);
    messageHist.innerHTML += `<p class='bot'><b>Bot:</b> Sorry, something went wrong.</p>`;
  }
}

async function clearChat() {
  const messageHist = document.getElementById("messageHistory");
  messageHist.innerHTML = "";
}

window.sendMessage = sendMessage;
window.clearChat = clearChat;