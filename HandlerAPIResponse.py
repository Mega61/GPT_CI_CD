import HandlerThreadMessage as ThMsgHandler
import requests
import os
from time import sleep
from dotenv import load_dotenv
import re

load_dotenv()

openai_api_key = os.getenv('OPEN_AI_API_KEY')

headers = {
    "Authorization": f"Bearer {openai_api_key}",
    "OpenAI-Beta": "assistants=v1"
}


def check_run_status(thread_id, run_id):
    url = f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error checking run status: {response.text}")


def get_thread_messages(thread_id):
    url = f"https://api.openai.com/v1/threads/{thread_id}/messages"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error retrieving thread messages: {response.text}")


def extract_gpt_response(response):

    geqi_match = re.search(r"GEQI=\[(\d+\.?\d*)\]", response)
    geqi = float(geqi_match.group(1)) if geqi_match else None

    recommendations = response

    return geqi, recommendations


def process_thread(thread_id, run_id):
    while True:
        run_status = check_run_status(thread_id, run_id)
        if run_status.get("status") == "completed":
            messages_response = get_thread_messages(thread_id)
            assistant_messages = ThMsgHandler.extract_assistant_messages(
                messages_response)

            return extract_gpt_response(assistant_messages)
        elif run_status.get("status") in ["failed", "cancelled"]:
            return {"status": "Run failed or cancelled"}
        else:
            print("Run not completed yet, checking again in 25 seconds...")
            sleep(25)
