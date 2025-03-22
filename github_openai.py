import os
from openai import OpenAI

def chat(user_message):
    """Gets a response from GPT-4o in real-time, making it sound friendly."""
    token = os.environ["GITHUB_TOKEN"]  # Ensure this is set in .env
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o"

    client = OpenAI(
        base_url=endpoint,
        api_key=token,
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You're a friendly and casual AI assistant. "
                    "Talk like a best friend, keeping the conversation natural, engaging, and fun. "
                    "Avoid using unnecessary symbols like @#$%^&*. "
                    "Your responses should be smooth and conversational, just like a normal human chat."
                ),
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        model=model_name,
        stream=True,
        stream_options={'include_usage': True}
    )

    full_response = ""
    for update in response:
        if update.choices and update.choices[0].delta:
            content = update.choices[0].delta.content or ""
            print(content, end="", flush=True)
            full_response += content  # Store full response

    print("\n")  # Add spacing after response
    return full_response  # Return the full response
