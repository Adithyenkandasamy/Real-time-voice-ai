from openai import OpenAI

class GPTModel:
    def __init__(self, api_key, endpoint):
        self.client = OpenAI(api_key=api_key, base_url=endpoint)
        self.full_transcript = [
            {"role": "system", "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."},
        ]

    def generate_ai_response(self, user_input):
        """ Process user input and generate AI response """
        if user_input in ["stop", "exit", "shutdown"]:
            print("🛑 Shutting down AI Assistant.")
            return

        self.full_transcript.append({"role": "user", "content": user_input})
        print(f"\n👤 User: {user_input}")

        response = self.client.chat.completions.create(
            model="gpt-4o",  # Use GPT-4o from GitHub's API
            messages=self.full_transcript
        )

        # Extract AI response
        ai_response = response.choices[0].message.content
        print(f"🤖 AI: {ai_response}")
        return ai_response
