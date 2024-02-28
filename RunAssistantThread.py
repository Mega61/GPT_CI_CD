from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def runAssistantThread(thread_id, asistant_id):
    try:
        client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=asistant_id,
        )
        print('Run creado: ' + run.id)
        return thread_id, run.id
    except Exception as e:
        print(f"Ha ocurrido un error creando el run: {e}")
        return None
