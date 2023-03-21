import React, { useRef, useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Chat from "./components/Chat/Chat";
import ChatInfo from "./components/ChatInfo/ChatInfo";
import InputForm from "./components/InputForm/InputForm";
import Navbar from "./components/Navbar/Navbar";
import Settings from "./settings/Settings";
import "./App.css";
import { fetchSystemMessage, resetSession, pollResult, callGpt, addMessage } from './apiUtils';

function App() {
  const [inputHeight, setInputHeight] = useState(0);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [apiEndpoint, setApiEndpoint] = useState("http://localhost:5000");
  const [pollingInterval, setPollingInterval] = useState(50);
  const chatRef = useRef(null);
  const [systemMessage, setSystemMessage] = useState("");

	useEffect(() => {
	  const fetchInitialSystemMessage = async () => {
		try {
		  const message = await fetchSystemMessage(apiEndpoint);
		  setSystemMessage(message);
		} catch (error) {
		  console.error("Error fetching system message:", error);
		}
	  };
	  
	  fetchInitialSystemMessage();
	}, [apiEndpoint]);

  
  return (
    <Router>
      <div className="App">
        <Navbar onResetSession={() => () => resetSession(apiEndpoint, setMessages)} />
        <Routes>
          <Route
            path="/settings"
            element={
              <Settings
                apiEndpoint={apiEndpoint}
                pollingInterval={pollingInterval}
                setApiEndpoint={setApiEndpoint}
                setPollingInterval={setPollingInterval}
                systemMessage={systemMessage}
                setSystemMessage={setSystemMessage}
              />
            }
          />
          <Route
            path="/"
            element={
              <>
                <div className="chat-container">
                  <ChatInfo messages={messages} />
                  <Chat messages={messages} />
                  <InputForm
					onUserMessage={(content) => callGpt(apiEndpoint, content, pollingInterval, setMessage, setMessages)}
                    onAiMessage={(message) => addMessage(message, "ai", setMessages)}
					message={message}
					setMessage={setMessage}
                  />
                </div>
              </>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
