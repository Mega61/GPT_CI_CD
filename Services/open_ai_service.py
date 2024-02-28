from openai import OpenAI


class Open_ai_service:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def create_thread(self):
        return self.client.beta.threads.create()

    def add_message(self, thread_id, message_content):
        return self.client.beta.threads.messages.create(
            thread_id,
            role="user",
            content=message_content
        )

    def create_run(self, thread_id, assistant_id):
        return self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

    def get_run(self, thread_id, run_id):
        return self.client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )

    def get_messages(self, thread_id):
        return self.client.beta.threads.messages.list(
            thread_id
        )
