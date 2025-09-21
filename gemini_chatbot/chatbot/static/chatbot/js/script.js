async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const message = userInput.value.trim();
    if (!message) return;

    const messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML += `<div class='message user'>${message}</div>`;
    userInput.value = "";

    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    const response = await fetch(`/get-response/?message=${encodeURIComponent(message)}`);
    const data = await response.json();

    messagesDiv.innerHTML += `<div class='message bot'>${data.response}</div>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
    