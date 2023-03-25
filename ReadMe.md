# Python Server with React Frontend

This project is a Python server with a React frontend. It features a chat application powered by the chatGPT model, and a user interface that allows for easy interaction with the AI.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher

### Installation

1. Clone the repository:

```
git clone https://github.com/bortlip/chat-buddy.git
```

2. Navigate to the `python-server` directory and install the required Python packages:

```
cd python-server
pip install -r requirements.txt
```

3. Set the OpenAI API key as an environment variable:

For Windows:
```
set OPENAI_API_KEY=your_api_key_here
```

For Linux and macOS:
```
export OPENAI_API_KEY=your_api_key_here
```

4. Navigate to the `react-frontend` directory and install the required Node.js packages:

```
cd ../react-frontend
npm install
```

## Running the Application

1. Start the Python server from the `python-server` directory:

```
python -m main
```

2. In a separate terminal, start the React development server from the `react-frontend` directory:

```
cd react-frontend
npm start
```

3. Open your browser and navigate to `http://localhost:3000` to access the application.

## Project Structure

- `python-server`: Contains the Python server files, including the chatGPT wrapper and API.
- `react-frontend`: Contains the React frontend files, including components, hooks, and styles.

