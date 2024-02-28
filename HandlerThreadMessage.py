def extract_assistant_messages(response):
    assistant_messages = []

    for message in response.get("data", []):
        if message.get("role") == "assistant":
            content = message.get("content", [])
            for item in content:
                if item.get("type") == "text":
                    text_content = item.get("text", {}).get("value", "")
                    assistant_messages.append(text_content)

    return "\n".join(assistant_messages)


