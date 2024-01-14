function sendMessage() {
    var user_input = document.getElementById("user_input").value;

    // Add user message to the chat
    var user_message = document.createElement("li");
    user_message.className = "user-message";

    // Append the user input text
    user_message.appendChild(document.createTextNode("You: " + user_input));

    // Append the user_message to the chat container
    document.getElementById("chat").appendChild(user_message);

    // Clear the input field
    document.getElementById("user_input").value = "";

    // Make an AJAX request to the server to get the bot's response
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/chat", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var bot_response = xhr.responseText;

            // Add bot message to the chat
            var bot_message = document.createElement("li");
            bot_message.className = "bot-message";

            // Append the bot response text
            bot_message.appendChild(document.createTextNode(bot_response));

            // Append the bot_message to the chat container
            document.getElementById("chat").appendChild(bot_message);

            // Scroll to the bottom of the chat
            scrollChatToBottom();
        }
    };
    xhr.send("user_input=" + encodeURIComponent(user_input));
}

function sendMessageOnEnter(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent the default behavior of the Enter key (e.g., new line)
        sendMessage();
    }
}

function scrollChatToBottom() {
    var chatContainer = document.getElementById("chat");
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Attach the function to the keypress event of the input field
document.getElementById("user_input").addEventListener("keypress", sendMessageOnEnter);
