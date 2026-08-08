import { useState } from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

import { FiCopy, FiCheck } from "react-icons/fi";


function CopyButton({ code }) {
  const [copied, setCopied] = useState(false);

  const copyCode = async () => {
    try {
      await navigator.clipboard.writeText(code);

      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 2000);

    } catch (error) {
      console.error("Copy failed:", error);
    }
  };

  return (
    <button
      className="copy-btn"
      onClick={copyCode}
      title="Copy Code"
    >
      {copied ? <FiCheck /> : <FiCopy />}
    </button>
  );
}


function ChatMessage({ sender, text }) {

  return (
    <div className={`message ${sender}`}>

      {/* IMPORTANT:
          ReactMarkdown is wrapped inside message-content
          so Markdown elements don't become flex columns.
      */}

      <div className="message-content">

        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{

            code({ inline, className, children, ...props }) {

              const match =
                /language-(\w+)/.exec(className || "");

              // Code block
              if (!inline && match) {

                const code =
                  String(children).replace(/\n$/, "");

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

              // Inline code
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
          {text}
        </ReactMarkdown>

      </div>

    </div>
  );
}

export default ChatMessage;