from huggingface_hub import InferenceClient

client = InferenceClient(
    "microsoft/Phi-3.5-mini-instruct",
    token="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",
)

def get_trivia_question(topic):
    question = ""
    for message in client.chat_completion(
    	messages=[{
            "role": "user", 
            "content": f"Give me a trivia question about {topic}. Only provide the question."
        }],
    	max_tokens=500,
    	stream=True,
    ):
        question+= message.choices[0].delta.content
    return question

def get_answer_rating(question, answer):
    response = ""
    for message in client.chat_completion(
    	messages=[{
            "role": "user", 
            "content": f"I was given this question: {question}. I provided this answer: {answer}. Give me a percentage of correctness."
        }],
    	max_tokens=500,
    	stream=True,
    ):
        response+= message.choices[0].delta.content
    return response

