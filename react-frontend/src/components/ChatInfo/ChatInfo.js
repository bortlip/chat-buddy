import React, { useEffect, useState } from "react";

function ChatInfo({ messages }) {
  const [messageCount, setMessageCount] = useState(0);
  const [wordCount, setWordCount] = useState(0);

  useEffect(() => {
    setMessageCount(messages.length);

    const totalWords = messages.reduce((count, message) => {
      return count + message.content.split(' ').length;
    }, 0);
    setWordCount(totalWords);
  }, [messages]);

  return (
    <div className="chat-info">
      <p>Total Messages: {messageCount}</p>
      <p>Total Word Count: {wordCount}</p>
    </div>
  );
}

export default ChatInfo;
