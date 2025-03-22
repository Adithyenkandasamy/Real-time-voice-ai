import os
import openai

def chat(user_message):
    """Gets a response from DeepSeek-R1 or GPT-4o in real-time."""
    token = os.getenv("GITHUB_TOKEN")  # Ensure this is set in .env
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "DeepSeek-R1"  # Change to "gpt-4o" if using OpenAI

    client = openai.AzureOpenAI(  # Use Azure's client
        api_key=token,
        api_version="2023-05-15",  # Azure requires API version
        azure_endpoint=endpoint
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You're a friendly AI assistant, speaking casually."},
            {"role": "user", "content": user_message},
        ],
        stream=True  # Enable streaming
    )

    full_response = ""
    for chunk in response:
        if chunk.choices and chunk.choices[0].delta:
            content = chunk.choices[0].delta.get("content", "")
            print(content, end="", flush=True)
            full_response += content  # Store the full response

    print("\n")  # Add spacing after response
    return full_response
