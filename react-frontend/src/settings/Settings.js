import React from "react";

function Settings({
  apiEndpoint,
  pollingInterval,
  setApiEndpoint,
  setPollingInterval,
  systemMessage,
  setSystemMessage,
}) {
  const handleApiEndpointChange = (e) => {
    setApiEndpoint(e.target.value);
  };

  const handlePollingIntervalChange = (e) => {
    setPollingInterval(parseInt(e.target.value));
  };

  const handleSystemMessageChange = (e) => {
    setSystemMessage(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Save settings to localStorage or a database

    // Save system message to the API
    try {
      await fetch(`${apiEndpoint}/api/system-message`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          prompt: systemMessage,
        }),
      });
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Settings</h1>
      <form onSubmit={handleSubmit}>
        <label>
          API Endpoint:
          <input
            type="text"
            value={apiEndpoint}
            onChange={handleApiEndpointChange}
          />
        </label>
        <br />
        <label>
          Polling Interval (ms):
          <input
            type="number"
            value={pollingInterval}
            onChange={handlePollingIntervalChange}
          />
        </label>
        <br />
        <label>
          System Message:
          <input
            type="text"
            value={systemMessage}
            onChange={handleSystemMessageChange}
          />
        </label>
        <br />
        <button type="submit">Save</button>
      </form>
    </div>
  );
}

export default Settings;
