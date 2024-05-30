import json

def parse_message_content(content):
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"commentary": content}