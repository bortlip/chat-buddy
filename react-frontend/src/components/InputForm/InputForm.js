import React from "react";
import TextareaAutosize from "react-textarea-autosize";
import "./InputForm.css";

function InputForm({ onUserMessage, onAiMessage, message, setMessage }) {

  const handleUserMessage = () => {
    onUserMessage(message);
    setMessage("");
  };

  const handleAiMessage = () => {
    onAiMessage(message);
    setMessage("");
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        setMessage("");
      }}
    >
      <div className="input-area">
        <TextareaAutosize
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleUserMessage();
            }
          }}
          placeholder="Type your message here..."
          minRows={10}
          maxRows={40}
        />
        <div className="button-container">
          <button type="button"
            onClick={handleUserMessage}
          >
            Send as User
          </button>
          <button
            type="button"
            onClick={handleAiMessage}
          >
            Send as AI
          </button>
        </div>
      </div>
    </form>
  );
}

export default InputForm;