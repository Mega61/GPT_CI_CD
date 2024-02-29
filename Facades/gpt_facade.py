import os
from dotenv import load_dotenv
from time import sleep
from Services.open_ai_service import Open_ai_service
import json

class GPT_Facade:

    def __init__(self) -> None:
        load_dotenv()
        openai_api_key = os.getenv('OPEN_AI_API_KEY')
        self.open_ai_service = Open_ai_service(openai_api_key)

    def complete_interaction(self, message_content, assistant_id):
        thread_id = self.open_ai_service.create_thread().id
        print('created thread ' + thread_id)
        self.open_ai_service.add_message(thread_id, message_content)
        run_id = self.open_ai_service.create_run(thread_id, assistant_id).id
        response_message = self.process_conversation(thread_id, run_id)
        return response_message, thread_id

    def continue_conversation(self, message_content, thread_id, assistant_id):
        self.open_ai_service.add_message(thread_id, message_content)
        run_id = self.open_ai_service.create_run(thread_id, assistant_id).id
        response_message = self.process_conversation(thread_id, run_id)
        return response_message

    def process_conversation(self, thread_id, run_id):
        while True:
            run = self.open_ai_service.get_run(thread_id, run_id)
            if run.status == "completed":
                messages_response = self.get_last_message(thread_id)

                return messages_response
            elif run.status in ["failed", "cancelled"]:
                return {"status": "Run failed or cancelled"}
            else:
                print("Run not completed yet, checking again in 10 seconds...")
                sleep(10)

    def get_last_message(self, thread_id):

        thread_messages = self.open_ai_service.get_messages(thread_id).data

        if thread_messages:
            for message in thread_messages:
                if message.role == 'assistant':  # Check if the message is from the assistant
                    if message.content and message.content[0].type == 'text':
                        text_content = message.content[0].text.value
                        return text_content
            return "No relevant assistant message found."
        else:
            return "No messages found in the thread."

    def get_assistant_id(self, json_file, assistant_id):
        with open(json_file, 'r') as file:
            data = json.load(file)
            return data.get(assistant_id)
