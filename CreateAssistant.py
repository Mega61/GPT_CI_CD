from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()


instruction_prompts = os.getenv('ASSISTANT_INSTRUCTIONS')
custom_knowledge_file = os.getenv('CUSTOM_KNOWLEDGE')

def create_assitant():
    try:
        client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

        file = client.files.create(
            file=open(custom_knowledge_file, "rb"),
            purpose='assistants'
        )
   
        assistant = client.beta.assistants.create(
            instructions=instruction_prompts,
            model="gpt-4-1106-preview",
            tools=[{"type": "code_interpreter"}],
            file_ids=[file.id]
        )
        return assistant
    except Exception as e:
        print(f"Ha ocurrido un error creando el asistente: {e}")
        return None
    
def write_assistant_id_to_json(assistant_id):
    with open('assistant_id.json', 'w') as file:
        json.dump({'assistant_id': assistant_id}, file)

def main():
    assistant = create_assitant()
    if assistant:
        print(f"Assistant created successfully. ID: {assistant.id}")
        write_assistant_id_to_json(assistant.id)

if __name__ == "__main__":
    main()