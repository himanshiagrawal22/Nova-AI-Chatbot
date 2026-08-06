export async function streamChat(message, onChunk) {
  const response = await fetch("http://127.0.0.1:8000/chat/stream", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
    }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();

    if (done) break;

    const chunk = decoder.decode(value);

    onChunk(chunk);
  }
}

export async function uploadPDF(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    "http://127.0.0.1:8000/upload-pdf",
    {
      method: "POST",
      body: formData,
    }
  );

  return await response.json();
}