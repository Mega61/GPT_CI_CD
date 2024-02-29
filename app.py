from flask import Flask, request, jsonify
from Facades.gpt_facade import GPT_Facade
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route('/')
def status_check():
    return 'Server is running!'


@app.route('/agorai_assistant', methods=['POST'])
def agorai_assistant():
    data = request.json
    user_message = data['user_message']

    try:
        gpt_handler = GPT_Facade()
        agorai_response, thread_id = gpt_handler.complete_interaction(
            user_message,
            gpt_handler.get_assistant_id('assistant_id.json', 'agorai'))
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
            user_message,
            thread_id,
            gpt_handler.get_assistant_id('assistant_id.json', 'agorai'))
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "bot_response": agorai_response,
        "thread_id": thread_id
    })


if __name__ == '__main__':
    app.run(debug=True)
