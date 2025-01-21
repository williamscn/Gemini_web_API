const form = document.getElementById('chat-form');
const messages = document.getElementById('messages');
const userInput = document.getElementById('user-input');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userMessage = userInput.value;
    addMessage(userMessage, 'user-message');
    userInput.value = '';

    const botResponse = await getBotResponse(userMessage);
    addMessage(botResponse, 'bot-message');
});

function addMessage(text, className) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    messageDiv.textContent = text;
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
}

async function getBotResponse(message) {
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message }),
        });
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        const data = await response.json();
        return data.reply;
    } catch (error) {
        console.error('Error fetching response:', error);
        return 'Sorry, something went wrong. Please try again later.';
    }
}

