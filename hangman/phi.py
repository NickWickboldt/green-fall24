from huggingface_hub import InferenceClient
import random

client = InferenceClient(
    "microsoft/Phi-3.5-mini-instruct",
    token="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",
)

def force_new_random_prompt():
    random_value = int(random.random() * 52) + 65
    random_character = chr(random_value)
    return random_character

def get_random_word():
    character = force_new_random_prompt()
    print(character)
    for message in client.chat_completion(
    	messages=[{
            "role": "user", 
            "content": f"Give me one random word for a game of hangman. Say nothing else besides the word. {character}"
            }],
    	max_tokens=500,
    	stream=True,
    ):
        print(message.choices[0].delta.content, end="")

get_random_word()