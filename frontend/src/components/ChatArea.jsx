import React, { useEffect, useRef } from "react";

import ChatMessage from "./ChatMessage";

function ChatArea({ messages }) {

  const messagesEndRef = useRef(null);

  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });

  }, [messages]);

  return (

    <div className="chat-area">

      {messages.length === 0 ? (

        <div className="welcome-screen">

          <h2>Hello, I'm Nova 👋</h2>

          <p>
            Upload a PDF or ask me anything.
          </p>

        </div>

      ) : (

        messages.map((msg, index) => (

          <ChatMessage
            key={index}
            sender={msg.sender}
            text={msg.text}
          />

        ))

      )}

      <div ref={messagesEndRef}></div>

    </div>

  );

}

export default ChatArea;