export const fetchSystemMessage = async (apiEndpoint) => {
	try {
	  const response = await fetch(`${apiEndpoint}/api/system-message`);
	  const data = await response.json();
	  return data.message;
	} catch (error) {
	  console.error(error);
	}
};

export const resetSession = async (apiEndpoint, setMessages) => {
	setMessages([]);
	await fetch(`${apiEndpoint}/api/messages/clear`, {
		method: "POST",
		headers: {
		  "Content-Type": "application/json",
		},
	});
};

export const pollResult = async (apiEndpoint, result_id, messageID, pollingInterval, setMessages) => {
    try {
      const response = await fetch(`${apiEndpoint}/api/results/${result_id}`);
      const data = await response.json();

      addMessage(data.message, "AI", setMessages, messageID);
      if (!data.completed) {
        setTimeout(() => pollResult(apiEndpoint, result_id, messageID, pollingInterval, setMessages), pollingInterval);
      }
    } catch (error) {
      console.error(error);
    }
};

export const callGpt = async (apiEndpoint, content, pollingInterval, setMessage, setMessages) => {
    // Store the last message ID
    addMessage(content, "user", setMessages);
    setMessage("");

    try {
      const response = await fetch(`${apiEndpoint}/api/messages`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: encodeURIComponent(content),
          sender: "User",
        }),
      });

      const data = await response.json();
      const result_id = data.result_id;
      const messageID = addMessage("", "AI", setMessages);
	  console.log("messageId: " + messageID)
      setTimeout(() => pollResult(apiEndpoint, result_id, messageID, pollingInterval, setMessages));
    } catch (error) {
      console.error(error);
    }
};

export const addMessage = (content, sender, setMessages, message_id = null) => {
	console.log(message_id)
    const timestamp = new Date().toLocaleTimeString();
    if (message_id) {
      setMessages((prevMessages) =>
        prevMessages.map((message) => {
          if (message.id === message_id) {
            return { ...message, content, timestamp };
          }
          return message;
        })
      );
	  return message_id
    } else {
      const newMessage = { content, sender, timestamp, id: Date.now() };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
      return newMessage.id;
    }
};
