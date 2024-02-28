from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def createThread(user_message):
    try:
        client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))
        thread = client.beta.threads.create()
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role='user',
            content=user_message
        )
        print('Thread creado. ThreadId: ' +
              thread.id + ' MessageID: ' + message.id)
        return thread.id
    except Exception as e:
        print(f"Ha ocurrido un error creando el thread: {e}")
        return None
