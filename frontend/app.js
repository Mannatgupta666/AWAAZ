// DOM Elements
const messagesContainer = document.getElementById("messagesContainer");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const micButton = document.getElementById("micButton");
const attachButton = document.getElementById("attachButton");
const fileInput = document.getElementById("fileInput");

// State
let isRecording = false;
let recognition = null;

// Initialize Speech Recognition
if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    messageInput.value = transcript;

    // Automatically send the recognized text
    if (transcript.trim()) {
      handleSendMessage();
    }
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    isRecording = false;
    micButton.classList.remove("recording");

    let errorMessage = "Speech recognition error. Please try again.";
    if (event.error === "no-speech") {
      errorMessage = "No speech detected. Please try again.";
    } else if (event.error === "not-allowed") {
      errorMessage =
        "Microphone access denied. Please allow microphone access.";
    }
    alert(errorMessage);
  };

  recognition.onend = () => {
    isRecording = false;
    micButton.classList.remove("recording");
  };
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  messageInput.focus();
});

// Event Listeners
function setupEventListeners() {
  sendButton.addEventListener("click", handleSendMessage);
  messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  });

  micButton.addEventListener("click", handleVoiceInput);
  attachButton.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", handleFileUpload);
}

// Send Text Message
async function handleSendMessage() {
  const text = messageInput.value.trim();

  if (!text) return;

  addUserMessage(text);
  messageInput.value = "";

  // Show typing indicator while waiting for response
  showTypingIndicator();

  try {
    // Send message to backend API
    const response = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: text,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    removeTypingIndicator();

    // Display backend response
    if (data.response) {
      addBotMessage(data.response);
    } else if (data.message) {
      addBotMessage(data.message);
    } else {
      addBotMessage("I received your message. How can I help you?");
    }
  } catch (error) {
    console.error("Error communicating with backend:", error);
    removeTypingIndicator();
    addBotMessage(
      "Sorry, I'm having trouble connecting to the server. Please try again later.",
    );
  }
}

// Voice Input
function handleVoiceInput() {
  if (!recognition) {
    alert(
      "Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.",
    );
    return;
  }

  if (!isRecording) {
    // Start recording
    isRecording = true;
    micButton.classList.add("recording");

    try {
      recognition.start();
    } catch (error) {
      console.error("Error starting speech recognition:", error);
      isRecording = false;
      micButton.classList.remove("recording");
      alert("Could not start speech recognition. Please try again.");
    }
  } else {
    // Stop recording
    isRecording = false;
    micButton.classList.remove("recording");
    recognition.stop();
  }
}

// File Upload
async function handleFileUpload(event) {
  const file = event.target.files[0];

  if (!file) return;

  if (!file.type.startsWith("image/")) {
    alert("Please upload an image file.");
    return;
  }

  // Display document preview in chat
  const reader = new FileReader();
  reader.onload = (e) => {
    addDocumentMessage(file.name, e.target.result);
  };
  reader.readAsDataURL(file);

  // Show typing indicator while uploading
  showTypingIndicator();

  try {
    // Create FormData to send file
    const formData = new FormData();
    formData.append("file", file);

    // Send document to backend API
    const response = await fetch("http://localhost:8000/api/upload-document", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    removeTypingIndicator();

    // Display verification result
    if (data.status === "success" || data.verification_status === "valid") {
      let resultMessage = "✅ Document verified successfully!\n\n";

      if (data.document_type) {
        resultMessage += `Document Type: ${data.document_type}\n`;
      }

      if (data.extracted_fields) {
        resultMessage += "\nExtracted Information:\n";
        for (const [key, value] of Object.entries(data.extracted_fields)) {
          resultMessage += `• ${key}: ${value}\n`;
        }
      }

      if (data.message) {
        resultMessage += `\n${data.message}`;
      }

      addBotMessage(resultMessage);
    } else if (
      data.status === "error" ||
      data.verification_status === "invalid"
    ) {
      let errorMessage = "❌ Document verification failed.\n\n";

      if (data.validation_errors && data.validation_errors.length > 0) {
        errorMessage += "Issues found:\n";
        data.validation_errors.forEach((error) => {
          errorMessage += `• ${error}\n`;
        });
      } else if (data.message) {
        errorMessage += data.message;
      } else {
        errorMessage += "Please upload a clear image of your document.";
      }

      addBotMessage(errorMessage);
    } else {
      addBotMessage(data.message || "Document uploaded successfully!");
    }
  } catch (error) {
    console.error("Error uploading document:", error);
    removeTypingIndicator();
    addBotMessage(
      "Sorry, I couldn't process your document. Please make sure the image is clear and try again.",
    );
  }

  // Reset file input
  fileInput.value = "";
}

// Add User Message
function addUserMessage(message) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message user";

  const bubbleDiv = document.createElement("div");
  bubbleDiv.className = "message-bubble";

  const textDiv = document.createElement("div");
  textDiv.className = "message-text";
  textDiv.textContent = message;

  const timeDiv = document.createElement("div");
  timeDiv.className = "message-time";
  timeDiv.textContent = getCurrentTime();

  bubbleDiv.appendChild(textDiv);
  bubbleDiv.appendChild(timeDiv);
  messageDiv.appendChild(bubbleDiv);

  messagesContainer.appendChild(messageDiv);
  scrollToBottom();
}

// Add Bot Message
function addBotMessage(message) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message bot";

  const bubbleDiv = document.createElement("div");
  bubbleDiv.className = "message-bubble";

  const textDiv = document.createElement("div");
  textDiv.className = "message-text";
  textDiv.textContent = message;

  const timeDiv = document.createElement("div");
  timeDiv.className = "message-time";
  timeDiv.textContent = getCurrentTime();

  bubbleDiv.appendChild(textDiv);
  bubbleDiv.appendChild(timeDiv);
  messageDiv.appendChild(bubbleDiv);

  messagesContainer.appendChild(messageDiv);
  scrollToBottom();
}

// Add Message to Chat (legacy function for compatibility)
function addMessage(text, sender) {
  if (sender === "user") {
    addUserMessage(text);
  } else {
    addBotMessage(text);
  }
}

// Add Document Message
function addDocumentMessage(fileName, imageData) {
  const messageDiv = document.createElement("div");
  messageDiv.className = "message user";

  const bubbleDiv = document.createElement("div");
  bubbleDiv.className = "message-bubble";

  const textDiv = document.createElement("div");
  textDiv.className = "message-text";
  textDiv.textContent = "📄 Document uploaded";

  const docPreview = document.createElement("div");
  docPreview.className = "document-preview";
  docPreview.textContent = fileName;

  const img = document.createElement("img");
  img.src = imageData;
  img.alt = fileName;
  docPreview.appendChild(img);

  const timeDiv = document.createElement("div");
  timeDiv.className = "message-time";
  timeDiv.textContent = getCurrentTime();

  bubbleDiv.appendChild(textDiv);
  bubbleDiv.appendChild(docPreview);
  bubbleDiv.appendChild(timeDiv);
  messageDiv.appendChild(bubbleDiv);

  messagesContainer.appendChild(messageDiv);
  scrollToBottom();
}

// Typing Indicator
function showTypingIndicator() {
  const typingDiv = document.createElement("div");
  typingDiv.className = "message bot";
  typingDiv.id = "typingIndicator";

  const bubbleDiv = document.createElement("div");
  bubbleDiv.className = "message-bubble";

  const indicatorDiv = document.createElement("div");
  indicatorDiv.className = "typing-indicator";
  indicatorDiv.innerHTML =
    '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

  bubbleDiv.appendChild(indicatorDiv);
  typingDiv.appendChild(bubbleDiv);

  messagesContainer.appendChild(typingDiv);
  scrollToBottom();
}

function removeTypingIndicator() {
  const indicator = document.getElementById("typingIndicator");
  if (indicator) {
    indicator.remove();
  }
}

// Utility Functions
function getCurrentTime() {
  const now = new Date();
  return now.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

// Scroll to Bottom
function scrollToBottom() {
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
