import os
from openai import OpenAI
from dotenv import load_dotenv
from time import sleep


class GPT_Facade:

    def __init__(self) -> None:
        load_dotenv()
        openai_api_key = os.getenv('OPEN_AI_API_KEY')
        self.client = OpenAI(api_key=openai_api_key)

    def complete_interaction(self, message_content, assistant_id):
        thread_id = self.create_thread().id
        print('created thread ' + thread_id)
        self.add_message(thread_id, message_content)
        run_id = self.create_run(thread_id, assistant_id).id
        response_message = self.process_conversation(thread_id, run_id)
        return response_message, thread_id

    def continue_conversation(self, message_content, thread_id, assistant_id):
        self.add_message(thread_id, message_content)
        run_id = self.create_run(thread_id, assistant_id).id
        response_message = self.process_conversation(thread_id, run_id)
        return response_message

    def process_conversation(self, thread_id, run_id):
        while True:
            run = self.get_run(thread_id, run_id)
            if run.status == "completed":
                messages_response = self.get_last_message(thread_id)

                return messages_response
            elif run.status in ["failed", "cancelled"]:
                return {"status": "Run failed or cancelled"}
            else:
                print("Run not completed yet, checking again in 10 seconds...")
                sleep(10)

    def get_last_message(self, thread_id):
        thread_messages_response = self.client.beta.threads.messages.list(
            thread_id)
        # Assuming 'data' is a property or method
        thread_messages = thread_messages_response.data

        if thread_messages:
            for message in thread_messages:
                if message.role == 'assistant':  # Check if the message is from the assistant
                    if message.content and message.content[0].type == 'text':
                        text_content = message.content[0].text.value
                        return text_content
            return "No relevant assistant message found."
        else:
            return "No messages found in the thread."

    def create_thread(self):
        thread = self.client.beta.threads.create()
        print(thread.id)
        return thread

    def add_message(self, thread, message_content):
        thread_message = self.client.beta.threads.messages.create(
            thread,
            role="user",
            content=message_content
        )
        return thread_message

    def create_thread_run(self, message_content, assistant_id):
        run = self.client.beta.threads.create_and_run(
            assistant_id=assistant_id,
            thread={
                "messages": [
                    {
                        "role": "user",
                        "content": message_content
                    }
                ]
            }
        )
        return run

    def create_run(self, thread_id, assistant_id):
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        return run

    def get_run(self, thread_id, run_id):
        run = self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run
