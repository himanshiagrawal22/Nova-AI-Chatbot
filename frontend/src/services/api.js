const API_URL = "http://127.0.0.1:8000";

// ================================
// STREAM CHAT
// ================================

export async function streamChat(message, onChunk) {
  const response = await fetch(`${API_URL}/chat/stream`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: message,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();

    console.error("Chat API Error:", response.status, errorText);

    throw new Error(`Chat API failed: ${response.status}`);
  }

  if (!response.body) {
    throw new Error("No response body received.");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();

    if (done) break;

    const chunk = decoder.decode(value, { stream: true });

    if (chunk) {
      onChunk(chunk);
    }
  }
}
// ================================
// UPLOAD PDF
// ================================

export async function uploadPDF(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_URL}/upload-pdf`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorText = await response.text();

    console.error(
      "PDF Upload Error:",
      response.status,
      errorText
    );

    throw new Error(`PDF upload failed: ${response.status}`);
  }

  return await response.json();
}


// ================================
// REMOVE PDF
// ================================

export async function removePDF() {
  const response = await fetch(`${API_URL}/remove-pdf`, {
    method: "DELETE",
  });

  if (!response.ok) {
    const errorText = await response.text();

    console.error(
      "Remove PDF Error:",
      response.status,
      errorText
    );

    throw new Error(`Remove PDF failed: ${response.status}`);
  }

  return await response.json();
}