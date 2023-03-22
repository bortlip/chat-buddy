import React, { useState } from 'react';
import './PromptModal.css';

function PromptModal({ isOpen, prompts, onSelectPrompt, onClose }) {
  const [selectedPrompt, setSelectedPrompt] = useState(null);

  const handleDisplayPrompt = (prompt) => {
    setSelectedPrompt(prompt);
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Select a System Prompt</h2>
        <div className="modal-flex-container">
          <div className="modal-section">
            <div className="modal-label-container">
              <label className="modal-section-title">Name</label>
              <ul className="prompt-list">
                {prompts.map((prompt, index) => (
                  <li
                    key={index}
                    onClick={() => onSelectPrompt(prompt)}
                    onMouseOver={() => handleDisplayPrompt(prompt)}
                  >
                    {prompt.name}
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="modal-section">
            <div className="modal-label-container">
              <label className="modal-section-title">Prompt</label>
              <textarea
                readOnly
                className="prompt-textbox"
                value={selectedPrompt ? selectedPrompt.prompt : ''}
              />
            </div>
          </div>
        </div>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default PromptModal;
