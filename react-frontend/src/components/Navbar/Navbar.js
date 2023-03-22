import React, { useState, useEffect } from 'react';
import { Link } from "react-router-dom";
import "./Navbar.css";
import PromptModal from '../Modals/PromptModal.jsx';

function Navbar({ onResetSession }) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [prompts, setPrompts] = useState([]);

  useEffect(() => {
    const fetchPrompts = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/initial-prompts');
        const data = await response.json();
        setPrompts(data);
      } catch (error) {
        console.error('Error fetching prompts:', error);
      }
    };

    fetchPrompts();
  }, []);

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleSelectPrompt = (prompt) => {
    sendSystemMessage(prompt.prompt, "system");     
    handleCloseModal();
  };

  const sendSystemMessage = async (prompt, role) => {
    try {
      const response = await fetch('http://localhost:5000/api/system-message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt, role }),
      });
  
      const data = await response.json();
  
      if (data.status === 'ok') {
        console.log('System message set successfully');
      } else {
        console.error('Error setting system message:', data);
      }
    } catch (error) {
      console.error('Error setting system message:', error);
    }
  };

  return (
    <>
      <nav>
        <ul>
          <li>
            <Link to="/">Chat</Link>
          </li>
          <li>
            <Link to="/settings">Settings</Link>
          </li>
          <li className="dropdown">
            <a href="" className="dropdown-toggle">
              Actions
            </a>
            <ul className="dropdown-menu">
              <li>
                <a onClick={() => onResetSession()()}>Reset Session</a>
              </li>
              <li>
                <a onClick={handleOpenModal}>Select Prompt</a>
              </li>
              <li>
                <a href="">Action 3</a>
              </li>
            </ul>
          </li>
        </ul>
      </nav>
      <PromptModal
        isOpen={isModalOpen}
        prompts={prompts}
        onSelectPrompt={handleSelectPrompt}
        onClose={handleCloseModal}
      />      
    </>
  );
}

export default Navbar;
