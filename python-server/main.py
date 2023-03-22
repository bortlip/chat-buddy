import uuid
import time
import threading

from flask import Flask, jsonify, request
from flask_cors import CORS
from urllib.parse import unquote
from my_module.agent import GPT35Agent
from my_module.agent_settings import AgentSettings
from my_module.role import Role
from my_module.initial_prompt import InitialPrompt

app = Flask(__name__)
CORS(app)

results = {}

@app.route("/api/initial-prompts", methods=["GET"])
def get_items():
    prompts = [
        InitialPrompt("Assistant", "You are a helpful assistant."),
        InitialPrompt("Friend", "You are a person and my friend.  Only respond as a person.  Always stay in character."),
    ]
    return jsonify([{"name": prompt.name, "prompt": prompt.prompt} for prompt in prompts])

def process_stream(result_id, response_stream):
    current_result = ""
    for chunk in response_stream:
        current_result += chunk
                
        with app.app_context():
            results[result_id] = {
                'message': current_result,
                'completed': False
            }

    with app.app_context():
        results[result_id] = {
            'message': current_result,
            'completed': True
        }

@app.route('/api/messages', methods=['POST'])
def add_message():
    data = request.get_json()
    content = unquote(data['content'])
    
    agent.add_user_message(content) 
    response_stream = agent.step_session_stream()
    
    result_id = str(uuid.uuid4())
    results[result_id] = {'message': "", 'completed': False}
    
    thread = threading.Thread(target=process_stream, args=(result_id, response_stream,))
    thread.start()

    response = jsonify({"result_id": result_id})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

@app.route('/api/results/<string:result_id>', methods=['GET'])
def get_result(result_id):
    result = results.get(result_id)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Result not found"}), 404

@app.route('/api/messages/clear', methods=['POST'])
def clear_messages():
    agent.clear_messages()
    return jsonify({'status': 'ok'})

@app.route('/api/system-message', methods=['GET'])
def get_system_message():
    result = jsonify({'message': agent.system_message.content})
    return result;

@app.route('/api/system-message', methods=['POST'])
def set_system_message():
    data = request.get_json()
    prompt = (data['prompt'])
    role = data.get('role', Role.SYSTEM.value)
    agent.set_system_message(prompt, role)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    instructions = """
    You answer questions based on a provided context.
"""
    settings = AgentSettings(instructions, "summaryAgent", 2000, 3000, 0.0, 3900)
    agent = GPT35Agent(settings)
    app.run(debug=True)