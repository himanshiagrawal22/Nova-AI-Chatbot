import "./App.css";
import { useState, useEffect, useRef } from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

import { FiCopy, FiCheck } from "react-icons/fi";

import { streamChat } from "./services/api";

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

  const messagesEndRef = useRef(null);

  const sendMessage = async () => {

    if (loading) return;

    if (message.trim() === "") return;

    const currentMessage = message;

    setLoading(true);

    setMessage("");

    // Add user message + empty bot message
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

          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            text: updated[updated.length - 1].text + chunk,
          };

          return updated;

        });

      });

    } catch (error) {

      console.error(error);

      setMessages((prev) => {

        const updated = [...prev];

        updated[updated.length - 1] = {
          sender: "bot",
          text: "❌ Something went wrong.",
        };

        return updated;

      });

    } finally {

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

      <div className="chat-box">

        {messages.length === 0 ? (

          <div className="message bot">
            Hello! I'm Nova. 👋
          </div>

        ) : (

          messages.map((msg, index) => (

            <div
              key={index}
              className={`message ${msg.sender}`}
            >

              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  code({ inline, className, children, ...props }) {

                    const match = /language-(\w+)/.exec(className || "");

                    if (!inline && match) {

                      const code = String(children).replace(/\n$/, "");

                      return (

                        <div className="code-block">

                          <div className="code-header">

                            <span>{match[1].toUpperCase()}</span>

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
                      <code className={className} {...props}>
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

        )}

        <div ref={messagesEndRef}></div>

      </div>

      <div className="input-area">

        <input
          type="text"
          placeholder="Ask Nova anything..."
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
          {loading ? "Generating..." : "Send"}
        </button>

      </div>

    </div>
  );

}

export default App;