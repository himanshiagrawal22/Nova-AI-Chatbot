import "./App.css";
import { useState, useEffect, useRef } from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

import { FiCopy, FiCheck } from "react-icons/fi";

import {
  streamChat,
  uploadPDF,
} from "./services/api";

function CopyButton({ code }) {

  const [copied, setCopied] = useState(false);

  const copyCode = async () => {

    await navigator.clipboard.writeText(code);

    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 2000);

  };

  return (

    <button
      className="copy-btn"
      onClick={copyCode}
      title="Copy code"
    >
      {copied ? <FiCheck /> : <FiCopy />}
    </button>

  );

}

function App() {

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const [uploading, setUploading] = useState(false);
  const [uploadedPDF, setUploadedPDF] = useState("");

  const messagesEndRef = useRef(null);

  // ------------------------
  // Upload PDF
  // ------------------------

  const handlePDFUpload = async (file) => {

    if (!file) return;

    if (file.type !== "application/pdf") {

      alert("Please upload a PDF.");

      return;

    }

    try {

      setUploading(true);

      const result = await uploadPDF(file);

      if (result.success) {

        setUploadedPDF(result.filename);

        setMessages(prev => [

          ...prev,

          {
            sender: "bot",
            text:
              `📄 **${result.filename}** uploaded successfully.\n\nYou can now ask questions about this document.`,
          }

        ]);

      }

      else {

        alert(result.message);

      }

    }

    catch (err) {

      console.error(err);

      alert("Upload failed.");

    }

    finally {

      setUploading(false);

    }

  };

  // ------------------------
  // Send Message
  // ------------------------

  const sendMessage = async () => {

    if (loading) return;

    if (!message.trim()) return;

    const currentMessage = message;

    setLoading(true);

    setMessage("");

    setMessages(prev => [

      ...prev,

      {
        sender: "user",
        text: currentMessage,
      },

      {
        sender: "bot",
        text: "",
      }

    ]);

    try {

      await streamChat(currentMessage, (chunk) => {

        setMessages(prev => {

          const updated = [...prev];

          updated[updated.length - 1] = {

            ...updated[updated.length - 1],

            text:

              updated[updated.length - 1].text + chunk,

          };

          return updated;

        });

      });

    }

    catch (error) {

      console.error(error);

      setMessages(prev => {

        const updated = [...prev];

        updated[updated.length - 1] = {

          sender: "bot",

          text: "❌ Something went wrong."

        };

        return updated;

      });

    }

    finally {

      setLoading(false);

    }

  };

  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({

      behavior: "smooth",

    });

  }, [messages]);

  return (

  <div className="app">

    <h1>Nova AI</h1>

    {/* ---------------------- */}
    {/* PDF Upload */}
    {/* ---------------------- */}

    <div className="upload-box">

      <input
        type="file"
        accept=".pdf"
        id="pdfUpload"
        hidden
        onChange={(e) => {

          handlePDFUpload(e.target.files[0]);

          e.target.value = "";

        }}
      />

      <label
        htmlFor={uploading ? "" : "pdfUpload"}
        className="upload-card"
      >

        <div className="upload-icon">

          📄

        </div>

        <div className="upload-text">

          <h3>

            {uploadedPDF

              ? "PDF Loaded"

              : "Upload PDF"}

          </h3>

          <p>

            {uploading

              ? "Uploading..."

              : uploadedPDF

              ? uploadedPDF

              : "Click here to upload your PDF"}

          </p>

        </div>

      </label>

    </div>

    {/* ---------------------- */}
    {/* Chat */}
    {/* ---------------------- */}

    <div className="chat-box">

      {

        messages.length === 0

          ? (

            <div className="message bot">

              Hello! I'm Nova. 👋

            </div>

          )

          : (

            messages.map((msg, index) => (

              <div

                key={index}

                className={`message ${msg.sender}`}

              >

                <ReactMarkdown

                  remarkPlugins={[remarkGfm]}

                  components={{

                    code({

                      inline,

                      className,

                      children,

                      ...props

                    }) {

                      const match = /language-(\w+)/.exec(className || "");

                      if (!inline && match) {

                        const code = String(children).replace(/\n$/, "");

                        return (

                          <div className="code-block">

                            <div className="code-header">

                              <span>

                                {match[1].toUpperCase()}

                              </span>

                              <CopyButton code={code} />

                            </div>

                            <SyntaxHighlighter

                              language={match[1]}

                              style={oneDark}

                              PreTag="div"

                              {...props}

                            >

                              {code}

                            </SyntaxHighlighter>

                          </div>

                        );

                      }

                      return (

                        <code

                          className={className}

                          {...props}

                        >

                          {children}

                        </code>

                      );

                    },

                  }}

                >

                  {msg.text}

                </ReactMarkdown>

              </div>

            ))

          )

      }

      <div ref={messagesEndRef}></div>

    </div>
        {/* ---------------------- */}
    {/* Input Area */}
    {/* ---------------------- */}

    <div className="input-area">

      <input
        type="text"
        placeholder={
          uploadedPDF
            ? `Ask anything about ${uploadedPDF}...`
            : "Ask Nova anything..."
        }
        value={message}
        disabled={loading}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {

          if (e.key === "Enter") {

            sendMessage();

          }

        }}
      />

      <button

        onClick={sendMessage}

        disabled={loading}

      >

        {loading

          ? "Generating..."

          : "Send"}

      </button>

    </div>

  </div>

);

}

export default App;