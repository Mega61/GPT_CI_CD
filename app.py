from flask import Flask, request, jsonify
from dotenv import load_dotenv
import CreateThread
import RunAssistantThread
import HandlerAPIResponse as apiHandler
import json
from Facades.gpt_facade import GPT_Facade
from flask_cors import CORS

load_dotenv()


app = Flask(__name__)
CORS(app)


@app.route('/review_code', methods=['POST'])
def review_code():
    data = request.json
    code_snippet = data['code']

    try:
        thread_id, run_id = RunAssistantThread.runAssistantThread(
            CreateThread.createThread(code_snippet), get_assistant_id('assistant_id.json'))
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        thread_id, run_id = None

    geqi, recommendations = apiHandler.process_thread(thread_id, run_id)
    markdown_creator(run_id, recommendations)
    return jsonify({"geqi": geqi, "recommendations": recommendations})


@app.route('/agorai_assistant', methods=['POST'])
def agorai_assistant():
    data = request.json
    user_message = data['user_message']

    try:
        gpt_handler = GPT_Facade()
        agorai_response, thread_id = gpt_handler.complete_interaction(
            user_message, get_assistant_id('assistant_id.json', 'agorai'))
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "bot_response": agorai_response,
        "thread_id": thread_id
    })


@app.route('/agorai_assistant_continue', methods=['POST'])
def agorai_assistant_continue():
    data = request.json
    user_message = data['user_message']
    thread_id = data['thread_id']

    try:
        gpt_handler = GPT_Facade()
        agorai_response = gpt_handler.continue_conversation(
            user_message, thread_id, get_assistant_id('assistant_id.json', 'agorai'))
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "bot_response": agorai_response,
        "thread_id": thread_id
    })


def markdown_creator(run_id, recommendations):
    with open('md_recommendations/code_review'+run_id+'.md', 'w') as md_file:
        md_file.write(recommendations)

    print("Markdown file created successfully.")


def get_assistant_id(json_file, assistant_id):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data.get(assistant_id)


if __name__ == '__main__':
    app.run(debug=True)
