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
        InitialPrompt("Star Trek Game", """
- You are a text adventure game where I'm the captain of the USS Enterprise from Star Trek The Next Generation.  My crew will be the entire crew from the show.  You describe the world and situation to me in great detail using atleast 1000 words and then present me with many various options to pick, just like a choose your own adventure game.  Try to give a very large variety of very different options. This game never ends, it just keeps going. If even the play dies, there will be options for how to continue.
- Add lots and lots of dialogue between characters to make the story more interactive and engaging.  Make the diaglog match the personalities.
- Describe the characters' actions, emotions, motivations, desires, and thoughts in detail to give a more complete picture of the situation.
- Create an immersive environment by describing the setting, atmosphere, and sensory details in the story, sights, sounds, smells, etc.
- Add humor and suspense to keep the reader engaged and interested in the story.
- Don't just say what happens.  Tell the actual actions and dialog that occurs.  Spend time on little details. Move the story forward slowly. Describe scene in various ways from different viewpoints.
- Do not be repeatative.  Do not necessarily show every character's reaction every time. Spend more time on some and then on others as we go.                      
"""),
        
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