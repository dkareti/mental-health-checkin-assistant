async function sendMessage() {
  const input = document.getElementById("userInput");
  const chatBox = document.getElementById("chatBox");
  const message = input.value;

  if (!message) return; // Don't send empty messages

  input.value = "";

  // Display user's message
  chatBox.innerHTML += `<p class='user'><b>You:</b> ${message}</p>`;

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
    chatBox.innerHTML += `<p class='bot'><b>Bot:</b> ${data.reply}</p>`;

  } catch (error) {
    console.error("Error sending message:", error);
    chatBox.innerHTML += `<p class='bot'><b>Bot:</b> Sorry, something went wrong.</p>`;
  }
}