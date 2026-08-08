import "./App.css";
import { useState } from "react";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import ChatArea from "./components/ChatArea";
import InputBar from "./components/InputBar";

import {
  streamChat,
  uploadPDF,
  removePDF,
} from "./services/api";

function App() {
  // ------------------------
  // State
  // ------------------------

  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const [uploading, setUploading] = useState(false);

  const [uploadedPDF, setUploadedPDF] = useState("");

  const [dragActive, setDragActive] = useState(false);


  // ------------------------
  // Upload PDF
  // ------------------------

  const handlePDFUpload = async (file) => {
    if (!file) return;

    // Check file type
    if (file.type !== "application/pdf") {
      alert("Please upload a PDF.");
      return;
    }

    try {
      setUploading(true);

      const result = await uploadPDF(file);

      if (result.success) {
        setUploadedPDF(result.filename);

        setMessages((prev) => [
          ...prev,
          {
            sender: "bot",
            text:
              `📄 **${result.filename}** uploaded successfully.\n\n` +
              `You can now ask questions about this document.`,
          },
        ]);
      } else {
        alert(result.message || "PDF upload failed.");
      }
    } catch (err) {
      console.error("PDF Upload Error:", err);

      alert("Upload failed.");
    } finally {
      setUploading(false);
      setDragActive(false);
    }
  };

  const handleNewChat = async () => {
  try {
    // Remove currently loaded PDF from backend
    if (uploadedPDF) {
      await removePDF();
    }
  } catch (error) {
    console.error("Error removing PDF:", error);
  }

  // Clear current chat
  setMessages([]);

  // Clear input
  setMessage("");

  // Clear uploaded PDF
  setUploadedPDF("");

  // Reset upload state
  setUploading(false);
};


  // ------------------------
  // Remove PDF
  // ------------------------

  const handleRemovePDF = async () => {
    try {
      const result = await removePDF();

      if (result.success) {
        setUploadedPDF("");

        setMessages((prev) => [
          ...prev,
          {
            sender: "bot",
            text: "📄 PDF removed successfully.",
          },
        ]);
      } else {
        alert(result.message || "Unable to remove PDF.");
      }
    } catch (err) {
      console.error("Remove PDF Error:", err);

      alert("Unable to remove PDF.");
    }
  };


  // ------------------------
  // Send Message
  // ------------------------

  const sendMessage = async () => {
    if (loading) return;

    if (!message.trim()) return;

    const currentMessage = message.trim();

    // Start loading
    setLoading(true);

    // Clear input
    setMessage("");

    // Add user message
    // Add empty bot message for streaming
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: currentMessage,
      },
      {
        sender: "bot",
        text: "",
      },
    ]);

    try {
      await streamChat(currentMessage, (chunk) => {
        setMessages((prev) => {
          const updated = [...prev];

          const lastMessage = updated[updated.length - 1];

          updated[updated.length - 1] = {
            ...lastMessage,
            text: lastMessage.text + chunk,
          };

          return updated;
        });
      });
    } catch (err) {
      console.error("Chat Error:", err);

      setMessages((prev) => {
        const updated = [...prev];

        updated[updated.length - 1] = {
          sender: "bot",
          text: "❌ Something went wrong. Please try again.",
        };

        return updated;
      });
    } finally {
      setLoading(false);
    }
  };


  // ------------------------
  // Render
  // ------------------------

  return (
    <div className="app">

      {/* ======================== */}
      {/* Sidebar */}
      {/* ======================== */}

      <Sidebar onNewChat={handleNewChat} />


      {/* ======================== */}
      {/* Main Content */}
      {/* ======================== */}

      <div className="main-content">

        {/* Header */}
        <Header
          uploadedPDF={uploadedPDF}
        />


        {/* Chat */}
        <ChatArea
          messages={messages}
        />


        {/* Input / PDF Upload */}
        <InputBar
          message={message}
          setMessage={setMessage}
          sendMessage={sendMessage}
          loading={loading}
          uploading={uploading}
          uploadedPDF={uploadedPDF}
          handlePDFUpload={handlePDFUpload}
          handleRemovePDF={handleRemovePDF}
          dragActive={dragActive}
          setDragActive={setDragActive}
        />

      </div>

    </div>
  );
}

export default App;