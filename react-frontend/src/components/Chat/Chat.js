import React, { useEffect, useRef } from "react";
import "./Chat.css";

function Chat({ messages }) {
  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div
      className="chat"
      ref={chatRef}
    >
      {messages.map((message) => (
        <div key={message.id} className="message">
          <span className="message-indicator">{message.timestamp}</span>
          <span className="message-indicator">{message.sender.toUpperCase()}</span>
          <div className={`message-content ${message.sender}`}>{message.content}</div>
        </div>
      ))}
    </div>
  );
}

export default Chat;
